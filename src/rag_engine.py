from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from src.config import VECTOR_STORE_DIR, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, OLLAMA_BASE_URL, RETRIEVER_K
from src.utils.logger import rag_logger, app_logger
import time

class RAGAnalyst:
    def __init__(self):
        app_logger.info("Initializing RAG Analyst Engine...")
        
        # 1. Embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
        # 2. Vector Store
        self.vectorstore = Chroma(
            persist_directory=str(VECTOR_STORE_DIR),
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
        
        # 3. LLM
        app_logger.info(f"Connecting to Ollama LLM: {LLM_MODEL_NAME}")
        self.llm = OllamaLLM(
            model=LLM_MODEL_NAME, 
            base_url=OLLAMA_BASE_URL,
            temperature=0.1 # Low temp for factual analysis
        )
        
        # 4. Prompt Template
        self.template = """
        당신은 선박 엔지니어링 전문가입니다. 주어진 Context를 바탕으로 알람 원인을 분석하고 해결책을 제시하세요.
        Context에 없는 내용은 지어내지 말고 "정보가 부족합니다"라고 말하세요.
        
        Context:
        {context}
        
        Current Sensor Data:
        {sensor_data}
        
        Alarm Code:
        {alarm_code}
        
        User Question:
        {question}
        
        Answer (Korean):
        """
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["context", "sensor_data", "alarm_code", "question"]
        )

    def analyze_situation(self, alarm_code: str, sensor_data: dict, question: str = "원인과 해결 방법을 요약해줘.") -> str:
        start_time = time.time()
        rag_logger.info(f"Analysis requested for Alarm: {alarm_code}")
        
        # 1. Retrieval
        query = f"Alarm {alarm_code}: {question}"
        # .invoke or .get_relevant_documents depending on langchain version
        # newer versions prefer invoke for retriever
        try:
            docs = self.retriever.invoke(query)
        except AttributeError:
             # Fallback for older versions
            docs = self.retriever.get_relevant_documents(query)
        
        rag_logger.debug(f"Retrieved {len(docs)} documents.")
        context_text = "\n\n".join([d.page_content for d in docs])
        
        for i, d in enumerate(docs):
            rag_logger.debug(f"Doc {i+1}: {d.metadata.get('source', 'Unknown')} - {d.page_content[:100]}...")
            
        # 2. Augmentation & Generation
        final_prompt = self.prompt.format(
            context=context_text,
            sensor_data=str(sensor_data),
            alarm_code=alarm_code,
            question=question
        )
        
        rag_logger.debug(f"Final Prompt Sent to LLM:\n{final_prompt}")
        
        try:
            response = self.llm.invoke(final_prompt)
            rag_logger.info("LLM Response received.")
            rag_logger.debug(f"Response: {response}")
            
            elapsed = time.time() - start_time
            rag_logger.info(f"Analysis completed in {elapsed:.2f} seconds.")
            
            return response
        except Exception as e:
            rag_logger.error(f"Error during RAG execution: {e}")
            return "시스템 오류로 인해 분석을 완료할 수 없습니다."
