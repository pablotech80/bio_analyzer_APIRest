# 🏛️ Arquitectura de Despliegue en Azure (Fase 0)

**Proyecto**: CoachBodyFit360 - Evolución a Plataforma SaaS Multi-Tenant  
**Owner**: Pablo Techera

---

## 🎯 Objetivo

Definir la infraestructura en la nube para CoachBodyFit360 sobre Microsoft Azure, garantizando una arquitectura **escalable, segura, resiliente y con una integración de IA de nivel empresarial** desde el primer día.

---

## Diagrama de Arquitectura de Alto Nivel

```mermaid
graph TD
    subgraph "Internet"
        User[👤 Usuario Final]
    end

    subgraph "Microsoft Azure Cloud"
        subgraph "VNet (Virtual Network)"
            subgraph "Public Subnet"
                AppGateway[Azure Application Gateway]
            end

            subgraph "Private Subnet 1 (App Services)"
                ContainerApp_Django[🚀 Azure Container App: Django/DRF]
                ContainerApp_Celery[⚡ Azure Container App: Celery Worker]
            end

            subgraph "Private Subnet 2 (Data Services)"
                AzurePG[🗄️ Azure DB for PostgreSQL]
                AzureRedis[🧠 Azure Cache for Redis]
            end
            
            subgraph "Private Subnet 3 (AI Services)"
                 AzureOpenAI[🤖 Azure OpenAI Service Endpoint]
            end

            AppGateway --> ContainerApp_Django
            ContainerApp_Django --> AzurePG
            ContainerApp_Django --> AzureRedis
            ContainerApp_Django --> BlobStorage
            ContainerApp_Django --> CommServices
            ContainerApp_Django -- Private Endpoint --> AzureOpenAI
            
            ContainerApp_Celery --> AzurePG
            ContainerApp_Celery --> AzureRedis
            ContainerApp_Celery --> CommServices
        end

        BlobStorage[📦 Azure Blob Storage]
        CommServices[✉️ Azure Communication Services (Email)]
        ACR[🐳 Azure Container Registry (ACR)]
    end

    subgraph "Vercel Cloud"
        NextJS[🌐 Frontend: Next.js]
    end

    subgraph "CI/CD Pipeline"
        GitHub[🐙 GitHub] -- Push --> GHActions[🤖 GitHub Actions]
    end

    User -- HTTPS --> NextJS
    NextJS -- API Calls --> AppGateway
    
    GHActions -- Build & Push --> ACR
    GHActions -- Deploy --> ContainerApp_Django
    GHActions -- Deploy --> ContainerApp_Celery

```

---

## 🛠️ Desglose de Componentes (Equivalencia AWS ➡️ Azure)

1.  **Frontend (Vercel)**:
    -   **Sin cambios**. Vercel sigue siendo la mejor opción para Next.js y se integra perfectamente con cualquier backend en la nube.

2.  **Computación (Azure Container Apps)**:
    -   **Equivalente a ECS on Fargate**. Es un servicio serverless para contenedores que simplifica el despliegue y escalado. Es más moderno y fácil de usar que ECS, con el poder de Kubernetes por debajo sin su complejidad.

3.  **Base de Datos (Azure Database for PostgreSQL)**:
    -   **Equivalente a RDS for PostgreSQL**. Servicio totalmente gestionado que se encarga de backups, seguridad y escalabilidad.

4.  **Caché y Tareas (Azure Cache for Redis)**:
    -   **Equivalente a ElastiCache for Redis**. Servicio gestionado de Redis para el broker de Celery y el caché de la aplicación.

5.  **Almacenamiento de Archivos (Azure Blob Storage)**:
    -   **Equivalente a AWS S3**. Almacenamiento de objetos altamente duradero y escalable para todos los archivos multimedia.

6.  **Red y Seguridad (VNet, Application Gateway)**:
    -   **Equivalente a VPC y Application Load Balancer**. La VNet aísla la infraestructura, y el Application Gateway actúa como balanceador de carga, firewall de aplicaciones web (WAF) y gestor de SSL.

7.  **Envío de Emails (Azure Communication Services)**:
    -   **Equivalente a AWS SES**. Servicio para enviar correos transaccionales de forma fiable y a escala.

8.  **Inteligencia Artificial (Azure OpenAI Service)**:
    -   **Ventaja Estratégica**. Proporciona un endpoint privado y seguro para los modelos de OpenAI (GPT-4o, etc.). Esto garantiza baja latencia, alta seguridad y cumplimiento normativo, algo imposible con la API pública.

---

## 🔄 CI/CD y DevOps

1.  **Infraestructura como Código (IaC)**:
    -   **Tecnología**: **Terraform**.
    -   **Propósito**: Se mantiene la decisión de usar Terraform. Definiremos toda la infraestructura de Azure (VNet, Container Apps, Azure PG, etc.) en código para una gestión predecible y versionada.

2.  **Integración y Despliegue Continuo (CI/CD)**:
    -   **Tecnología**: **GitHub Actions**.
    -   **Flujo**:
        1.  Un `push` a la rama `main` en GitHub dispara un workflow.
        2.  **Test**: Se ejecutan las pruebas unitarias y de integración.
        3.  **Build**: Se construye la imagen Docker de la aplicación Django.
        4.  **Push**: La imagen se sube a **Azure Container Registry (ACR)**.
        5.  **Deploy**: Se actualiza la revisión en Azure Container Apps para que use la nueva imagen, realizando un despliegue sin tiempo de inactividad.