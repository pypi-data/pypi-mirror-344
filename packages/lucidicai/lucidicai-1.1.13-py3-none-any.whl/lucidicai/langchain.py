"""Langchain integration for Lucidic API with detailed logging"""
from typing import Dict, Any, List, Optional, Union
from uuid import UUID
import traceback

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult, ChatGenerationChunk, GenerationChunk
from langchain_core.documents import Document

from .client import Client
from .model_pricing import calculate_cost

class LucidicLangchainHandler(BaseCallbackHandler):
    
    def __init__(self):
        """Initialize the handler with a Lucidic client.
        
        """
        # TODO: Remove need for client argument, grab singleton
        self.client = Client()
        # Keep track of which run is associated with which model
        self.run_to_model = {}
        # Keep track of which run is associated with which event
        self.run_to_event = {}
        print("[Handler] Initialized LucidicLangchainHandler")

    def _get_model_name(self, serialized: Dict, kwargs: Dict) -> str:
        """Extract model name from input parameters"""
        if "invocation_params" in kwargs and "model" in kwargs["invocation_params"]:
            return kwargs["invocation_params"]["model"]
        if serialized and "model_name" in serialized:
            return serialized["model_name"]
        if serialized and "name" in serialized:
            return serialized["name"]
        return "unknown_model"

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Handle start of LLM calls"""
        run_str = str(run_id)
        model = self._get_model_name(serialized, kwargs)
        self.run_to_model[run_str] = model
        
        description = f"LLM call ({model}): {prompts[0]}..." if prompts else "LLM call"
        
        # Make sure we have a valid session and step
        print(f"\n[DEBUG] on_llm_start for run_id {run_str}")
        print(f"[DEBUG] client session: {self.client.session}")
        if not (self.client.session and self.client.session.active_step):
            print(f"[DEBUG] Cannot create event - no active session or step")
            return
        
        print(f"[DEBUG] active_step: {self.client.session.active_step}")
        print(f"[DEBUG] event_history count: {len(self.client.session.active_step.event_history)}")
        
        # Print all events and their status
        for i, event in enumerate(self.client.session.active_step.event_history):
            print(f"[DEBUG] Event {i} id={event.event_id} finished={event.is_finished}")
            
        try:
            # Create a new event
            print(f"[DEBUG] Creating new event with description: {description}")
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_str] = event
            print(f"[DEBUG] Created new event with id={event.event_id}")
            
            # Check all events again after creation
            print(f"[DEBUG] After creation, event_history count: {len(self.client.session.active_step.event_history)}")
            for i, event in enumerate(self.client.session.active_step.event_history):
                print(f"[DEBUG] Event {i} id={event.event_id} finished={event.is_finished}")
                
        except Exception as e:
            print(f"[DEBUG] Error in event creation: {e}")
            print(traceback.format_exc())

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Handle start of chat model calls"""
        run_str = str(run_id)
        model = self._get_model_name(serialized, kwargs)
        self.run_to_model[run_str] = model
        
        # Format messages for description
        parsed_messages = []
        if messages and messages[0]:
            for msg in messages[0]:
                if hasattr(msg, 'type') and hasattr(msg, 'content'):
                    parsed_messages.append(f"{msg.type}: {msg.content}...")
        
        message_desc = "; ".join(parsed_messages[:2])
        description = f"Chat model call ({model}): {message_desc}"
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            print(f"[Handler] Cannot create event - no active session or step")
            return
            
        try:
            # Create a new event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_str] = event
            print(f"[Handler] Started event for run {run_str}")
        except Exception as e:
            print(f"[Handler] Error creating event: {e}")

    def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        **kwargs: Any
    ) -> None:
        """Handle streaming tokens"""
        # We don't need to track tokens for this implementation
        pass

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle end of LLM call"""
        run_str = str(run_id)
        model = self.run_to_model.get(run_str, "unknown")
        
        # Calculate cost if token usage exists
        cost = None
        if response.generations and response.generations[0]:
            message = response.generations[0][0].message
            usage = message.usage_metadata
            cost = calculate_cost(model, usage)
        
        # Make sure we have a valid session
        print(f"\n[DEBUG] on_llm_end for run_id {run_str}")
        if not (self.client.session and self.client.session.active_step):
            print(f"[DEBUG] Cannot end event - no active session or step")
            return
            
        print(f"[DEBUG] active_step: {self.client.session.active_step}")
        if self.client.session.active_step:
            print(f"[DEBUG] event_history count: {len(self.client.session.active_step.event_history)}")
        
        try:
            if run_str in self.run_to_event:
                event = self.run_to_event[run_str]
                print(f"[DEBUG] Found event for run_id {run_str}, id={event.event_id}")
                
                if not event.is_finished:
                    result = None
                    if message:
                        result = message.pretty_repr()
                        
                    event.end_event(
                        is_successful=True, 
                        cost_added=cost, 
                        model=model,
                        result=result
                    )
                    print(f"[DEBUG] Successfully finished event id={event.event_id}, result={result}, cost={cost}")
                else:
                    print(f"[DEBUG] Event already finished id={event.event_id}")
                
                del self.run_to_event[run_str]
            else:
                print(f"[DEBUG] No event found for run_id {run_str}")
        except Exception as e:
            print(f"[DEBUG] Error in event ending: {e}")
            print(traceback.format_exc())
            
        # Clean up
        if run_str in self.run_to_model:
            del self.run_to_model[run_str]

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Handle LLM errors"""
        run_str = str(run_id)
        model = self.run_to_model.get(run_str, "unknown")
        
        # Make sure we have a valid session
        if not (self.client.session and self.client.session.active_step):
            print(f"[Handler] Cannot end event - no active session or step")
            return
            
        try:
            if run_str in self.run_to_event:
                event = self.run_to_event[run_str]
                if not event.is_finished:
                    event.end_event(is_successful=False, model=model)
                    print(f"[Handler] Ended event with error for run {run_str}")
                del self.run_to_event[run_str]
            else:
                print(f"[Handler] No event found for run {run_str}")
        except Exception as e:
            print(f"[Handler] Error ending event: {e}")
            
        # Clean up
        if run_str in self.run_to_model:
            del self.run_to_model[run_str]

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """Handle start of chain execution"""
        run_str = str(run_id)
        chain_type = serialized.get("name", "Unknown Chain")
        input_desc = str(next(iter(inputs.values())))[:50] if inputs else "No inputs"
        
        description = f"Chain execution ({chain_type}): {input_desc}..."
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            print(f"[Handler] Cannot create event - no active session or step")
            return
            
        try:
            # Create a new event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_str] = event
            print(f"[Handler] Started chain event for run {run_str}")
        except Exception as e:
            print(f"[Handler] Error creating chain event: {e}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Handle end of chain execution"""
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session
        if not (self.client.session and self.client.session.active_step):
            print(f"[Handler] Cannot end event - no active session or step")
            return
        
        # Extract result from outputs
        result = None
        if outputs:
            # Try to get the first output value
            first_key = next(iter(outputs))
            output_value = outputs[first_key]
            
            # Convert to string if needed and truncate
            if output_value is not None:
                result = str(output_value)[:1000]
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=True, result=result)
                    print(f"[Handler] Ended chain event for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending chain event: {e}")

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        """Handle chain errors"""
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session
        if not (self.client.session and self.client.session.active_step):
            print(f"[Handler] Cannot end event - no active session or step")
            return
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=False)
                    print(f"[Handler] Ended chain event with error for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending chain event: {e}")

    # Simple implementations for remaining methods:
    def on_tool_start(self, serialized, input_str, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        tool_name = serialized.get("name", "Unknown Tool")
        description = f"Tool Call ({tool_name}): {input_str[:100]}..."
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
            
        try:
            # Create event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_id] = event
            print(f"[Handler] Started tool event for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error creating tool event: {e}")

    def on_tool_end(self, output, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
        
        # Get result from output
        result = None
        if output is not None:
            result = str(output)[:1000]
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=True, result=result)
                    print(f"[Handler] Ended tool event for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending tool event: {e}")

    def on_tool_error(self, error, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=False)
                    print(f"[Handler] Ended tool event with error for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending tool event: {e}")

    def on_retriever_start(self, serialized, query, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        retriever_type = serialized.get("name", "Unknown Retriever")
        description = f"Retriever ({retriever_type}): {query[:100]}..."
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
            
        try:
            # Create event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_id] = event
            print(f"[Handler] Started retriever event for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error creating retriever event: {e}")

    def on_retriever_end(self, documents, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
        
        # Extract result from documents
        result = None
        if documents:
            # Try to get a meaningful summary of retrieved documents
            try:
                doc_count = len(documents)
                sample = str(documents[0].page_content)[:200] if hasattr(documents[0], 'page_content') else str(documents[0])[:200]
                result = f"Retrieved {doc_count} documents. Sample: {sample}..."
            except (IndexError, AttributeError):
                # Fallback to simple string representation
                result = f"Retrieved {len(documents)} documents"
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=True, result=result)
                    print(f"[Handler] Ended retriever event for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending retriever event: {e}")

    def on_retriever_error(self, error, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
            
        try:
            if run_id in self.run_to_event:
                event = self.run_to_event[run_id]
                if not event.is_finished:
                    event.end_event(is_successful=False)
                    print(f"[Handler] Ended retriever event with error for run {run_id}")
                del self.run_to_event[run_id]
            else:
                print(f"[Handler] No event found for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error ending retriever event: {e}")

    def on_agent_action(self, action, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        tool = getattr(action, 'tool', 'unknown_tool')
        description = f"Agent Action: {tool}"
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
        
        # Extract useful information from the action
        result = None
        try:
            tool_input = getattr(action, 'tool_input', None)
            if tool_input:
                if isinstance(tool_input, dict):
                    # Format dictionary nicely
                    input_str = ", ".join(f"{k}: {v}" for k, v in tool_input.items())
                    result = f"Using tool '{tool}' with inputs: {input_str}"
                else:
                    result = f"Using tool '{tool}' with input: {str(tool_input)}"
            else:
                result = f"Using tool '{tool}'"
        except Exception:
            result = f"Using tool '{tool}'"
            
        try:
            # Create event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_id] = event
            
            # Note: Agent actions are immediately ended in the original code
            # This seems intentional so we'll keep the behavior but use our event
            if not event.is_finished:
                event.end_event(is_successful=True, result=result)
            del self.run_to_event[run_id]
            
            print(f"[Handler] Processed agent action for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error processing agent action: {e}")

    def on_agent_finish(self, finish, **kwargs):
        run_id = str(kwargs.get("run_id", "unknown"))
        description = "Agent Finish"
        
        # Make sure we have a valid session and step
        if not (self.client.session and self.client.session.active_step):
            return
        
        # Extract result from finish
        result = None
        try:
            if hasattr(finish, 'return_values'):
                if isinstance(finish.return_values, dict) and 'output' in finish.return_values:
                    result = str(finish.return_values['output'])[:1000]
                else:
                    result = str(finish.return_values)[:1000]
            elif hasattr(finish, 'output'):
                result = str(finish.output)[:1000]
        except Exception:
            pass
            
        try:
            # Create event
            event = self.client.session.create_event(description=description)
            self.run_to_event[run_id] = event
            
            # Note: Agent finish events are immediately ended in the original code
            # This seems intentional so we'll keep the behavior but use our event
            if not event.is_finished:
                event.end_event(is_successful=True, result=result)
            del self.run_to_event[run_id]
            
            print(f"[Handler] Processed agent finish for run {run_id}")
        except Exception as e:
            print(f"[Handler] Error processing agent finish: {e}")
    
    def attach_to_llms(self, llm_or_chain_or_agent) -> None:
        """Attach this handler to an LLM, chain, or agent"""
        # If it's a direct LLM
        if hasattr(llm_or_chain_or_agent, 'callbacks'):
            callbacks = llm_or_chain_or_agent.callbacks or []
            if self not in callbacks:
                callbacks.append(self)
                llm_or_chain_or_agent.callbacks = callbacks
                print(f"[Handler] Attached to {llm_or_chain_or_agent.__class__.__name__}")
                
        # If it's a chain or agent, try to find LLMs recursively
        for attr_name in dir(llm_or_chain_or_agent):
            try:
                if attr_name.startswith('_'):
                    continue
                attr = getattr(llm_or_chain_or_agent, attr_name)
                if hasattr(attr, 'callbacks'):
                    callbacks = attr.callbacks or []
                    if self not in callbacks:
                        callbacks.append(self)
                        attr.callbacks = callbacks
                        print(f"[Handler] Attached to {attr.__class__.__name__} in {attr_name}")
            except Exception as e:
                print(f"[Handler] Warning: Could not attach to {attr_name}: {e}")