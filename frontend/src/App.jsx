import { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    nome: '',
    objetivos: '',
    restricoes: '',
    diasPorSemana: 3,
    nivel: 'Iniciante'
  });

  const [workoutPlan, setWorkoutPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const generateWorkout = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setWorkoutPlan(null);

    try {
      const response = await axios.post('http://localhost:5000/api/generate-workout', formData);
      setWorkoutPlan(response.data);
    } catch (err) {
      console.error(err);
      setError('Erro ao gerar treino. Verifique se o backend está rodando e a chave do Gemini configurada.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">AI Gym Planner</h1>
        <p className="subtitle">Seu treino personalizado gerado por Inteligência Artificial</p>
      </div>

      <div className="glass-card">
        <form onSubmit={generateWorkout}>
          <div className="form-group">
            <label htmlFor="nome">Qual o seu nome?</label>
            <input 
              type="text" 
              id="nome" 
              name="nome" 
              className="form-control" 
              placeholder="Ex: João, Maria..."
              value={formData.nome}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="objetivos">O que você deseja melhorar no seu corpo?</label>
            <input 
              type="text" 
              id="objetivos" 
              name="objetivos" 
              className="form-control" 
              placeholder="Ex: Ganhar massa muscular, perder barriga..."
              value={formData.objetivos}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="restricoes">Possui alguma restrição médica ou dor?</label>
            <input 
              type="text" 
              id="restricoes" 
              name="restricoes" 
              className="form-control" 
              placeholder="Ex: Dor no joelho esquerdo, Nenhuma..."
              value={formData.restricoes}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="diasPorSemana">Dias disponíveis por semana</label>
            <select 
              id="diasPorSemana" 
              name="diasPorSemana" 
              className="form-control"
              value={formData.diasPorSemana}
              onChange={handleChange}
            >
              <option value="2">2 dias</option>
              <option value="3">3 dias</option>
              <option value="4">4 dias</option>
              <option value="5">5 dias</option>
              <option value="6">6 dias</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="nivel">Nível de experiência</label>
            <select 
              id="nivel" 
              name="nivel" 
              className="form-control"
              value={formData.nivel}
              onChange={handleChange}
            >
              <option value="Iniciante">Iniciante</option>
              <option value="Intermediário">Intermediário</option>
              <option value="Avançado">Avançado</option>
            </select>
          </div>

          {error && <p style={{color: '#f87171', marginTop: '1rem'}}>{error}</p>}

          <button type="submit" className="btn-generate" disabled={loading}>
            {loading ? (
              <><span className="loader"></span> Gerando Treino...</>
            ) : (
              'Gerar Meu Treino'
            )}
          </button>
        </form>

        {workoutPlan && workoutPlan.plano && (
          <div className="workout-results">
            <h2 className="title" style={{fontSize: '2rem', marginBottom: '2rem', textAlign: 'center'}}>Seu Plano de Treino</h2>
            
            {workoutPlan.plano.map((dia, idx) => (
              <div key={idx} className="workout-day">
                <h3 className="day-title">{dia.dia}</h3>
                <p className="day-focus">Foco: {dia.foco}</p>
                <ul className="exercise-list">
                  {dia.exercicios.map((ex, exIdx) => (
                    <li key={exIdx} className="exercise-item">
                      <span className="exercise-name">{ex.nome}</span>
                      <span className="exercise-details">{ex.series} séries x {ex.repeticoes} (Descanso: {ex.descanso})</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}

            {workoutPlan.dicas_extras && (
              <div className="extra-tips">
                <h3>💡 Dicas do Personal</h3>
                <ul>
                  {workoutPlan.dicas_extras.map((dica, idx) => (
                    <li key={idx}>{dica}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
