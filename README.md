# data-product-kg

# Setup :

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker run --rm -d --name my-neo4j  
-p 7474:7474 -p 7687:7687  
-e NEO4J\_AUTH=neo4j/password  
neo4j:5.18.1


sudo docker run --rm -d \
  --name my-neo4j \
  -p7474:7474 -p7687:7687 \
  -e NEO4J\_AUTH=neo4j/password \
  -e NEO4J\_dbms\_security\_procedures\_unrestricted=apoc.\*,apoc.meta.data \
  -e NEO4J\_dbms\_security\_procedures\_allowlist=apoc.\*,apoc.meta.data \
  -e NEO4J\_PLUGINS='\[\\"apoc\\"]' \
  neo4j:5.18.1

 sudo docker run --rm -d   --name my-neo4j   -p7474:7474 -p7687:7687   -e NEO4J_AUTH=neo4j/password   -e NEO4J_PLUGINS='["apoc"]'   -e NEO4J_dbms_security_procedures_unrestricted=apoc.*   -e NEO4J_dbms_security_procedures_allowlist=apoc.meta.data,apoc.*   neo4j:5.18.1


pip install py2neo pandas
pip install openai neo4j langchain streamlit

# Prompt to LLM:
(:DataProduct)-\[:FEEDS\_INTO]->(:DataProduct)
(:DataProduct)-\[:HAS\_PIPELINE]->(:Pipeline)
(:Pipeline)-\[:TRIGGERS]->(:Pipeline)
(:Pipeline)-\[:PRODUCES]->(:DataProduct)

# Neo4j Browser
http://localhost:7474/browser/

# 1 : Display Full KG:
MATCH (n)
OPTIONAL MATCH (n)-\[r]->(m)
RETURN n, r, m

# 2 : Show only DataProduct-related stuff  
MATCH (dp:DataProduct)
OPTIONAL MATCH (dp)-\[r]-(connected)
RETURN dp, r, connected

# 3: particular dataproduct with 2 levels
MATCH path=(dp:DataProduct {dataproduct\_id: "ba3448fd-9328-4503-9e16-3340a4e65167"})-\[\*1..2]-(related)
RETURN path

