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

--------------------------------------------------------------------------------------------------------------------------------------

<img width="1000" height="542" alt="image" src="https://github.com/user-attachments/assets/0d9a7107-7c6c-4b7f-b474-953c1cb028e2" />
<img width="1000" height="576" alt="image" src="https://github.com/user-attachments/assets/1c697675-30cd-4308-b0fd-156c2f21dcbd" />
<img width="992" height="541" alt="image" src="https://github.com/user-attachments/assets/3c7002b8-0603-464a-a78e-508d5b62a1ad" />
<img width="1000" height="576" alt="image" src="https://github.com/user-attachments/assets/291c9373-e815-4d32-b5f6-4cb198f79669" />
<img width="1000" height="576" alt="image" src="https://github.com/user-attachments/assets/438b70f9-5e3b-4b95-84f7-1c0afafc53ce" />
<img width="1000" height="576" alt="image" src="https://github.com/user-attachments/assets/7d30bf93-b77e-4e6f-bfe7-a85332071833" />
<img width="1000" height="576" alt="image" src="https://github.com/user-attachments/assets/825c341f-f7d5-460e-b0ad-d9b2575c9188" />
<img width="992" height="541" alt="image" src="https://github.com/user-attachments/assets/7e2b02a9-27b4-4912-a6f6-6135c3358eb6" />
<img width="1000" height="594" alt="image" src="https://github.com/user-attachments/assets/1d3d1453-d60c-46e4-bdde-365a46fb23d3" />









