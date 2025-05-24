import os
import asyncio
import uuid
from typing import Dict, List, Any
from loguru import logger

from agents import Agent, Runner, FileSearchTool, trace

class OpenAIHandler:
    """
    Handler for interacting with OpenAI API using the provided agent code.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.threads_manager = ThreadsManager()
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all the agent specialists."""
        # Create specialists for different hospital machines
        self.especialista_rpd = Agent(
            name="especialista_rpd",
            instructions="""Você é um especialista no aparelho terapêutico RPD. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_6830883c2cdc8191a069a7e015fb3746"],
                ),
            ],
        )

        self.especialista_neurospa = Agent(
            name="especialista_neurospa",
            instructions="""Você é um especialista no aparelho terapêutico NeuroSpa. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_683087d5e2bc819198ca08bf8564f120"],
                ),
            ],
        )

        self.especialista_ilib = Agent(
            name="especialista_ilib",
            instructions="""Você é um especialista no aparelho terapêutico Hidrovitállis Ilib. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_683086c3f5e88191828c4fc6afda9516"],
                ),
            ],
        )

        self.especialista_hidrovitalis_mini = Agent(
            name="especialista_hidrovitalis_mini",
            instructions="""Você é um especialista no aparelho terapêutico Hidrovitállis Mini. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_6830860231648191bbfec287104ed5cf"],
                ),
            ],
        )

        self.especialista_colorgenpro = Agent(
            name="especialista_colorgenpro",
            instructions="""Você é um especialista no aparelho terapêutica ColorGen Pro. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_682fe397104c81918614dd112fee7af0"],
                ),
            ],
        )

        self.especialista_prosync = Agent(
            name="especialista_prosync",
            instructions="""Você é um especialista no aparelho terapêutico ProSync. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_682fe32b72ec81918b9d9c1f133a9dd2"],
                ),
            ],
        )

        self.especialista_potentizer = Agent(
            name="especialista_potentizer",
            instructions="""Você é um especialista no aparelho terapêutico Potentizer. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            handoffs=[
                self.especialista_colorgenpro,
            ],
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_682fe210a2d8819194225fc4ab4397a0"],
                ),
            ],
        )

        self.especialista_pczapper = Agent(
            name="especialista_pczapper",
            instructions="""Você é um especialista no aparelho terapêutico PC-Zapper. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_682fe1ae0b40819188068f62e20f9343"],
                ),
            ],
        )

        self.especialista_hidrovitalis_master = Agent(
            name="especialista_hidrovitalis_master",
            instructions="""Você é um especialista no aparelho terapêutico Hidrovitális Master. Nunca informe ao usuário que as informações que você fornece foram obtidas de algum documento fornecido. Nunca faça nenhuma referência a documento fornecido. Você é o especialista.""",
            tools=[
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=["vs_682d4a4b8184819195ed73ba7e23de23"],
                ),
            ],
        )

        # Create the triage assistant
        self.assistente = Agent(
            name="assistente_triagem",
            instructions="""Você é um assistente virtual de um hospital especializado em encaminhar perguntas
            aos especialistas corretos. Analise cuidadosamente cada pergunta para identificar qual máquina hospitalar
            está sendo mencionada ou qual especialista seria mais apropriado para responder.
            
            Se a pergunta mencionar:
            - RPD → encaminhe para especialista_ressonancia
            - NeuroSpa → encaminhe para especialista_raio_x
            - Ilib → encaminhe para especialista_ultrassom
            - Hidrovitális Mini → encaminhe para especialista_ventilador
            - Color Gen Pro → encaminhe para especialista_monitor
            - ProSync → encaminhe para especialista_desfibrilador
            - PC Zapper → encaminhe para especialista_bomba
            - Potentizer → encaminhe para especialista_anestesia
            - Hidrovitális Master → encaminhe para especialista_dialise
            
            Se o equipamento não for claro ou a pergunta for genérica, peça mais detalhes antes de encaminhar.
            Seja amigável e profissional em todas as interações.""",
            handoffs=[
                self.especialista_rpd, 
                self.especialista_neurospa,
                self.especialista_ilib, 
                self.especialista_hidrovitalis_mini, 
                self.especialista_colorgenpro, 
                self.especialista_prosync, 
                self.especialista_potentizer, 
                self.especialista_pczapper,
                self.especialista_hidrovitalis_master
            ],
        )
        
    def process_message(self, user_id: str, message: str) -> str:
        """
        Process a user message and return the AI response.
        
        Args:
            user_id: ID of the user
            message: User's message
            
        Returns:
            AI response
        """
        try:
            # Use asyncio to run the async process_message function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self._process_message_async(user_id, message)
            )
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"Sorry, an error occurred: {str(e)}"
            
    async def _process_message_async(self, user_id: str, message: str) -> str:
        """
        Async implementation of message processing.
        
        Args:
            user_id: ID of the user
            message: User's message
            
        Returns:
            AI response
        """
        # Get or create the thread for this user
        thread = self.threads_manager.get_or_create_thread(user_id)
        
        # Add the user message to the thread
        thread.add_message("user", message)
        
        # Prepare the input list
        input_list = thread.get_input_list()
        
        full_response = ""
        
        # Always start with the triage assistant
        with trace("Hospital Equipment Support System - Triage", group_id=thread.thread_id):
            resultado_triagem = Runner.run_streamed(
                self.assistente,
                input=input_list,
            )
        
        # Get the specialist agent selected by triage
        agente_especialista = resultado_triagem.current_agent
        
        # Now run the specialist to generate the final response
        with trace("Hospital Equipment Support System - Specialist", group_id=thread.thread_id):
            resultado_especialista = Runner.run_streamed(
                agente_especialista,
                input=input_list,
            )
            
            # Collect the full response from the specialist
            async for evento in resultado_especialista.stream_events():
                from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
                from agents import RawResponsesStreamEvent
                
                if not isinstance(evento, RawResponsesStreamEvent):
                    continue
                dados = evento.data
                if isinstance(dados, ResponseTextDeltaEvent):
                    full_response += dados.delta
                elif isinstance(dados, ResponseContentPartDoneEvent):
                    pass
        
        # Add the assistant's response to the thread
        thread.add_message("assistant", full_response)
        
        # Reset the current agent to the triage assistant for the next message
        thread.current_agent = self.assistente
        
        return full_response


class Thread:
    """Represents a conversation thread with a user."""
    
    def __init__(self, user_id: str):
        self.thread_id = str(uuid.uuid4().hex[:16])
        self.user_id = user_id
        self.messages: List[Dict[str, Any]] = []
        self.current_agent = None
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the thread."""
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def get_input_list(self) -> List[dict]:
        """Convert messages to the format expected by the Runner."""
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]


class ThreadsManager:
    """Manages conversation threads for different users."""
    
    def __init__(self):
        self.threads: Dict[str, Thread] = {}
    
    def get_or_create_thread(self, user_id: str) -> Thread:
        """Get an existing thread or create a new one for a user."""
        if user_id not in self.threads:
            self.threads[user_id] = Thread(user_id)
        return self.threads[user_id]