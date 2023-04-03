# Piniverse

Steps to get integration working locally:

1. Git: git fetch; git checkout ModelGenerator; git pull (PowerShell) or 
 git fetch && git checkout ModelGenerator && git pull (CMD)

2. Update: OpenAI Token: 
My OpenAI token is just revoked as I pushed to our repo (public github repo). You now need to substitute your own API token if you wanna run. 

The token is located at ./OpenAIGenerator/generator_apis.py at line 4.
Instructions to get a token: https://beta.openai.com/account/api-keys

3. Follow either "DEV" or "Docker" in "How to run" to start

How to run:
DEV:
With running in dev mode, you need to have at least four sessions/terminals/processes

1. Frontend: Execute npm run dev under ./Frontend
2. API Server: Execute npm run dev under ./ApiGateway
3. ModelGenerator: Execute python -u server.py under ./ModelGenerator
4. OpenAI Module: Execute python -u server.py under ./OpenAIGenerator

Docker:
STRONGLY NOT RECOMMENDED DUE TO GPU ISSUE

1. at root folder, run docker compose up -d

How to test:

1. Go to frontend: If DEV, go to localhost:8081, if Docker, go to localhost
2. Input any string / story to the input field, and click generate. 
Recommended to type somewhere else and then copy to input box as the eventlistener for keys are attached to window, so if you opened console there will be lots of prints.
3. Wait a few. Now you can go to terminal (if dev) or docker logs (if docker) to see where it goes.
4. Some models will be generated after 20 minutes (docker with cpu on my end for 1 model) or after 1-2 minutes (dev on my end for 2 models)

OpenAI Module: There is a logs folder. You can check logs

How to control frontend viewport:
D for drag mode, 
W for object axis move mode (need to hover and select), 
E for rotate (hover & select), 
R for scaling (hover & select)
No camera movement control now
