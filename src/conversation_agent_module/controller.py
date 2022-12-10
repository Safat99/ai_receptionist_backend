from src.conversation_agent_module.conversation_agent_package.ConvAgent import ConvAgent



#using "multi-qa-distilbert-cos-v1" , accuracy : 0.99 
conversational_agent_module = ConvAgent("multi-qa-distilbert-cos-v1")

conversation_data = conversational_agent_module.conversation("ক্রেডিট ট্রান্সফার করতে চাই কি করতে হবে")
print(conversation_data)
