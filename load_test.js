import http from 'k6/http'; // Importa o módulo HTTP para fazer requisições
import { sleep, check } from 'k6'; // Importa funções para pausa e validações

// --- 1. Configurações do Teste (Opcional, mas recomendado para controle de carga) ---
export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Aumenta para 20 VUs em 30s
    { duration: '1m', target: 50 },  // Mantém 50 VUs por 1 minuto
    { duration: '30s', target: 0 },  // Diminui para 0 VUs em 30s
  ],
  // vus: 50, // Remova ou comente esta linha se usar 'stages'
  // duration: '2m', // Remova ou comente esta linha se usar 'stages'
};

// --- 2. Função Principal (O que cada usuário virtual vai fazer) ---
// Esta função é executada repetidamente por cada usuário virtual durante o teste.
export default function () {
  // Define a URL da sua aplicação para o teste
  // ATENÇÃO: Use o nome do serviço Docker Compose se sua aplicação estiver na mesma rede!
  const targetUrl = 'http://your-application:8080/';

  // Realiza uma requisição GET para o endpoint da sua aplicação
  const res = http.get(targetUrl);

  // Verifica a resposta da requisição
  // É crucial validar se a requisição foi bem-sucedida e se a resposta está correta
  check(res, {
    'status is 200': (r) => r.status === 200, // Verifica se o status HTTP é 200 (OK)
    'response body contains expected text': (r) => r.body && r.body.includes('Hello from Python Flask App!'), // Verifica se o corpo da resposta contém um texto específico
    'response time < 200ms': (r) => r.timings.duration < 200, // Verifica se o tempo de resposta foi menor que 200ms
  });

  // Pausa o usuário virtual por um tempo (para simular um comportamento mais realista)
  // Isso ajuda a não sobrecarregar o servidor com requisições consecutivas sem "intervalo"
  sleep(1); // Pausa por 1 segundo
}