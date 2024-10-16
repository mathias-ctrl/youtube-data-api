# YouTube Video Information and Download API

## Descrição
Esta API, construída com FastAPI, permite aos usuários obter informações detalhadas sobre vídeos do YouTube e baixar o áudio desses vídeos. Ela utiliza a API oficial do YouTube para recuperar metadados do vídeo e a biblioteca yt-dlp para o download de áudio.

## Funcionalidades
- Recuperar informações detalhadas de vídeos do YouTube, incluindo título, descrição, estatísticas e transcrição
- Baixar o áudio de vídeos do YouTube
- Endpoint de teste para verificar o status da API

## Pré-requisitos
- Python 3.7+
- Chave de API do YouTube
- Bibliotecas Python: fastapi, youtube_transcript_api, google-api-python-client, yt-dlp

## Instalação
1. Clone o repositório:
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio   

2. Instale as dependências:
pip install fastapi youtube_transcript_api google-api-python-client yt-dlp uvicorn

3. Configure sua chave de API do YouTube:
Substitua 'YOUR_API_KEY' no código pela sua chave de API real do YouTube.

## Uso
Para iniciar o servidor:
python main.py

O servidor será iniciado em `http://0.0.0.0:8000`.

## Endpoints da API

### 1. Obter Informações do Vídeo
- **URL**: `/video_info/{video_id}`
- **Método**: GET
- **Parâmetros de URL**: 
  - `video_id`: ID do vídeo do YouTube
- **Resposta de Sucesso**:
  - Código: 200
  - Conteúdo: JSON contendo informações detalhadas do vídeo

### 2. Baixar Áudio do Vídeo
- **URL**: `/download_video/{video_id}`
- **Método**: GET
- **Parâmetros de URL**: 
  - `video_id`: ID do vídeo do YouTube
- **Resposta de Sucesso**:
  - Código: 200
  - Conteúdo: JSON com mensagem de sucesso e caminho do arquivo baixado

### 3. Teste da API
- **URL**: `/test`
- **Método**: GET
- **Resposta de Sucesso**:
  - Código: 200
  - Conteúdo: `{"message": "API is working!"}`

## Configuração
- O logging está configurado para o nível INFO
- Os downloads são salvos no diretório 'downloads' na raiz do projeto
- A API do YouTube é configurada para buscar snippets, detalhes de conteúdo e estatísticas dos vídeos

## Tratamento de Erros
- A API inclui tratamento de erros para lidar com vídeos não encontrados, erros HTTP e exceções inesperadas
- Os erros são registrados no log para facilitar a depuração

## Contribuição
Contribuições são bem-vindas! Por favor, siga estes passos:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença
[Inclua aqui informações sobre a licença do seu projeto]

## Contato
[Seu Nome] - [seu-email@exemplo.com]

Link do Projeto: [https://github.com/seu-usuario/seu-repositorio](https://github.com/seu-usuario/seu-repositorio)
