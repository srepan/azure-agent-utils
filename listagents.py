from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Your Foundry project endpoint
#endpoint = "https://aifoundry1488.ai.azure.com/api/projects/project1488"
endpoint = "https://sreesdxai.services.ai.azure.com/api/projects/proj-sdx"
client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

agents = client.agents.list()

for agent in agents:
    data = agent._data

    latest = data.get("versions", {}).get("latest", {})
    identity = latest.get("instance_identity")

    if identity:
        print(f"Agent Name: {agent.name}")
        print("Instance Identity:", identity)
        print("-" * 50)

    if not identity:
        print(f"Agent Name: {agent.name}")
        print("No instance_identity")
        print("-" * 50)

#for agent in agents:
#    print("Agent Name:", agent.name)
#    if(agent.name == "MyMCPAgent4"):
       
#        print(vars(agent))
#        print("-" * 50)
#    if(agent.name == "jun18agent"):
#        print(vars(agent))
#        print("-" * 50)

    # ✅ GET versions (properties live here)
    #versions = agent.versions
    
    #for v in versions:
    #    print("  Version:", v.version)
    #    print("  Model:", v.definition.model)
    ##    print("  Instructions:", v.definition.instructions)
    #    print("  Tools:", [t.type for t in v.definition.tools])
    #    print("-----")
