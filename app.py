flowchart LR

%% ==========================
%% FRONTEND
%% ==========================
subgraph Frontend["🎬 Streamlit Frontend"]

Login["🔐 Login"]
Dashboard["📊 Dashboard"]

Movie["🎥 Movies"]
Music["🎵 Music Videos"]
Shorts["🎬 Short Films"]

Storyboard["📖 Storyboard"]
Timeline["🎞 Timeline"]
Assets["🖼 Asset Library"]

Billing["💳 Billing"]
Settings["⚙️ Settings"]

end

%% ==========================
%% API GATEWAY
%% ==========================
subgraph Gateway["🚪 FastAPI Gateway"]

Auth["Authentication"]
ProjectsAPI["Projects API"]
AssetsAPI["Assets API"]
BillingAPI["Billing API"]
AIAPI["AI API"]
Webhook["Stripe Webhook"]

end

%% ==========================
%% SERVICES
%% ==========================
subgraph Services["⚙️ Backend Services"]

ProjectService["Project Manager"]

AssetService["Asset Manager"]

CreditService["Credit Manager"]

RenderQueue["Render Queue"]

RenderWorker["AI Render Workers"]

Notification["Notification Service"]

end

%% ==========================
%% DATABASE
%% ==========================
subgraph Database["🗄 PostgreSQL"]

Users[(Users)]

Projects[(Projects)]

Scenes[(Scenes)]

AssetsDB[(Assets)]

Credits[(Credits)]

Transactions[(Transactions)]

Jobs[(Render Jobs)]

end

%% ==========================
%% STORAGE
%% ==========================
subgraph Storage["☁ Cloud Storage"]

Images[(Images)]

Videos[(Videos)]

Audio[(Audio)]

Exports[(Exports)]

end

%% ==========================
%% AI
%% ==========================
subgraph AI["🤖 AI Providers"]

OpenAI["OpenAI"]

Veo["Google Veo"]

Runway["Runway"]

Kling["Kling"]

ElevenLabs["ElevenLabs"]

end

%% ==========================
%% PAYMENTS
%% ==========================
subgraph Stripe["💳 Stripe"]

Checkout["Checkout"]

Payment["Payment"]

end

%% ==========================
%% FLOW
%% ==========================

Frontend --> Gateway

Gateway --> ProjectService
Gateway --> AssetService
Gateway --> CreditService

Gateway --> AIAPI

Gateway --> Database

ProjectService --> Projects
ProjectService --> Scenes

AssetService --> AssetsDB

AssetService --> Storage

CreditService --> Credits
CreditService --> Transactions

Billing --> Checkout

Checkout --> Payment

Payment --> Webhook

Webhook --> BillingAPI

BillingAPI --> CreditService

AIAPI --> RenderQueue

RenderQueue --> RenderWorker

RenderWorker --> OpenAI
RenderWorker --> Veo
RenderWorker --> Runway
RenderWorker --> Kling
RenderWorker --> ElevenLabs

RenderWorker --> Jobs

RenderWorker --> Videos
RenderWorker --> Images
RenderWorker --> Audio
RenderWorker --> Exports

Storage --> Dashboard

Jobs --> Dashboard

Credits --> Dashboard

Notification --> Dashboard
