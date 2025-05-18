import { useState, useEffect } from "react";
import axios from "axios";
import { FaSun, FaMoon, FaRocket, FaBook, FaUser, FaChartLine, FaRoad, FaShare } from "react-icons/fa";
import "./App.css";

function App() {
  const [profissao, setProfissao] = useState("");
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  // Verificar preferência de tema ao carregar
  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      setDarkMode(true);
      document.documentElement.classList.add("dark-theme");
    }
  }, []);

  // Alternar entre tema claro e escuro
  const toggleTheme = () => {
    if (darkMode) {
      document.documentElement.classList.remove("dark-theme");
      localStorage.setItem("theme", "light");
    } else {
      document.documentElement.classList.add("dark-theme");
      localStorage.setItem("theme", "dark");
    }
    setDarkMode(!darkMode);
  };

  const gerarDados = async () => {
    if (!profissao) {
      setErro("Por favor, digite uma profissão ou área de interesse.");
      return;
    }

    setErro("");
    setCarregando(true);
    setResultado(null);

    try {
      const response = await axios.post("http://localhost:5000/gerar_post", {
        profissao: profissao,
      });
      setResultado(response.data);
    } catch (error) {
      console.error("Erro na requisição:", error);
      setErro(
        "Erro ao conectar com o backend. Verifique se o servidor está rodando."
      );
    } finally {
      setCarregando(false);
    }
  };

  // Função para formatar texto com markdown básico
  const formatarTexto = (texto) => {
    if (!texto) return "";
    
    // Substituir **texto** por <strong>texto</strong>
    let formatado = texto.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    
    // Substituir quebras de linha por <br />
    formatado = formatado.replace(/\n/g, "<br />");
    
    return formatado;
  };

  // Função para compartilhar
  const compartilhar = () => {
    if (navigator.share) {
      navigator.share({
        title: `Mentoria para: ${profissao}`,
        text: `Confira minha mentoria de carreira para ${profissao} gerada pelo Mentor do Futuro!`,
        url: window.location.href,
      })
      .catch((error) => console.log('Erro ao compartilhar', error));
    } else {
      alert("Compartilhamento não suportado neste navegador");
    }
  };

  return (
    <div className="App">
      <div className="theme-toggle-container">
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Alternar tema">
          {darkMode ? <FaSun className="theme-icon" /> : <FaMoon className="theme-icon" />}
        </button>
      </div>

      <header className="header">
        <h1>Mentor do Futuro</h1>
        <p className="subtitle">Descubra seu caminho profissional com IA</p>
      </header>

      <div className="input-container">
        <input
          type="text"
          placeholder="Digite sua profissão ou área de interesse..."
          value={profissao}
          onChange={(e) => setProfissao(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && gerarDados()}
        />
        <button onClick={gerarDados} className="primary-button">
          <FaRocket className="button-icon" /> Gerar plano
        </button>
      </div>

      {erro && <div className="error-message">{erro}</div>}

      {carregando && (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Criando seu plano personalizado...</p>
        </div>
      )}

      {resultado && (
        <div className="resultado">
          <div className="resultado-header">
            <h2>Mentoria para: {profissao}</h2>
            <button onClick={compartilhar} className="share-button" aria-label="Compartilhar">
              <FaShare />
            </button>
          </div>

          <div className="section">
            <div className="section-title">
              <div className="section-icon">
                <FaUser />
              </div>
              <strong>Mentor</strong>
            </div>
            <div 
              className="section-content"
              dangerouslySetInnerHTML={{ __html: formatarTexto(resultado.mentor) }}
            />
          </div>

          <div className="section">
            <div className="section-title">
              <div className="section-icon">
                <FaBook />
              </div>
              <strong>Cursos</strong>
            </div>
            <div 
              className="section-content"
              dangerouslySetInnerHTML={{ __html: formatarTexto(resultado.cursos) }}
            />
            
            <div className="highlight">
              <p>
                💡 <strong>Dica:</strong> Comece pelos cursos fundamentais e
                avance gradualmente para os mais especializados.
              </p>
            </div>
          </div>

          <div className="section">
            <div className="section-title">
              <div className="section-icon">
                <FaUser />
              </div>
              <strong>Perfil</strong>
            </div>
            <div 
              className="section-content"
              dangerouslySetInnerHTML={{ __html: formatarTexto(resultado.perfil) }}
            />
          </div>

          <div className="section">
            <div className="section-title">
              <div className="section-icon">
                <FaChartLine />
              </div>
              <strong>Mercado</strong>
            </div>
            <div 
              className="section-content"
              dangerouslySetInnerHTML={{ __html: formatarTexto(resultado.mercado) }}
            />
          </div>

          <div className="section">
            <div className="section-title">
              <div className="section-icon">
                <FaRoad />
              </div>
              <strong>Trajetória</strong>
            </div>
            <div 
              className="section-content"
              dangerouslySetInnerHTML={{ __html: formatarTexto(resultado.trajetoria) }}
            />
          </div>
        </div>
      )}

      <footer className="footer">
        <p>© {new Date().getFullYear()} Mentor do Futuro - Desenvolvido com IA</p>
      </footer>
    </div>
  );
}

export default App;