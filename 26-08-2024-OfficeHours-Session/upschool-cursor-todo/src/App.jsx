import { useState } from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faCheck, faCalendarAlt, faClock } from '@fortawesome/free-solid-svg-icons';
import { Fireworks } from 'fireworks-js';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [newDeadline, setNewDeadline] = useState('');
  const [editIndex, setEditIndex] = useState(null);
  const [editText, setEditText] = useState('');

  const addTodo = () => {
    if (newTodo.trim()) {
      setTodos([...todos, { text: newTodo, completed: false, deadline: newDeadline }]);
      setNewTodo('');
      setNewDeadline('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addTodo();
    }
  };

  const deleteTodo = (index) => {
    setTodos(todos.filter((_, i) => i !== index));
  };

  const editTodo = (index) => {
    setEditIndex(index);
    setEditText(todos[index].text);
  };

  const updateTodo = () => {
    const updatedTodos = todos.map((todo, i) =>
      i === editIndex ? { ...todo, text: editText } : todo
    );
    setTodos(updatedTodos);
    setEditIndex(null);
    setEditText('');
  };

  const toggleComplete = (index) => {
    const updatedTodos = todos.map((todo, i) =>
      i === index ? { ...todo, completed: !todo.completed } : todo
    );
    setTodos(updatedTodos);
    if (!todos[index].completed) {
      triggerFireworks();
    }
  };

  const postponeTodo = (index) => {
    const updatedTodos = todos.map((todo, i) => {
      if (i === index) {
        const newDeadline = new Date(todo.deadline);
        newDeadline.setDate(newDeadline.getDate() + 7);
        return { ...todo, deadline: newDeadline.toISOString().split('T')[0] };
      }
      return todo;
    });
    setTodos(updatedTodos);
  };

  const triggerFireworks = () => {
    const container = document.createElement('div');
    container.className = 'fireworks-container';
    document.body.appendChild(container);

    const fireworks = new Fireworks(container, {
      rocketsPoint: {
        min: 50,
        max: 50
      }
    });

    fireworks.start();

    setTimeout(() => {
      fireworks.stop();
      document.body.removeChild(container);
    }, 1500);
  };

  const getDeadlineColor = (deadline) => {
    const now = new Date();
    const dueDate = new Date(deadline);
    const diffTime = dueDate - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays > 30) {
      return 'green';
    } else if (diffDays <= 30 && diffDays > 7) {
      return 'orange';
    } else if (diffDays <= 7 && diffDays > 1) {
      return 'red';
    } else if (diffDays === 1) {
      return 'heartbeat';
    } else {
      return 'red';
    }
  };

  return (
    <div className="app">
      <h1>Sketchy Todo List</h1>
      <div className="input-group">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Add a new todo"
        />
        <input
          type="date"
          value={newDeadline}
          onChange={(e) => setNewDeadline(e.target.value)}
          placeholder="Set a deadline"
        />
        <button onClick={addTodo} title="Add Todo">
          <FontAwesomeIcon icon={faPlus} />
        </button>
      </div>
      <ul className="todo-list">
        {todos.map((todo, index) => {
          const deadlineColor = getDeadlineColor(todo.deadline);
          return (
            <li
              key={index}
              className={`todo-item ${todo.completed ? 'completed' : ''} ${deadlineColor === 'heartbeat' ? 'heartbeat' : ''}`}
              style={{
                borderColor: deadlineColor === 'heartbeat' ? 'red' : deadlineColor,
                backgroundColor: new Date(todo.deadline) < new Date() ? 'red' : '#333',
              }}
            >
              {editIndex === index ? (
                <>
                  <input
                    type="text"
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                  />
                  <button onClick={updateTodo} title="Update Todo">
                    <FontAwesomeIcon icon={faCheck} />
                  </button>
                </>
              ) : (
                <>
                  <span onClick={() => toggleComplete(index)}>{todo.text}</span>
                  <span className="deadline">
                    <FontAwesomeIcon icon={faCalendarAlt} /> {todo.deadline}
                  </span>
                  <button onClick={() => editTodo(index)} title="Edit Todo">
                    <FontAwesomeIcon icon={faEdit} />
                  </button>
                  <button onClick={() => deleteTodo(index)} title="Delete Todo">
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                  <button onClick={() => postponeTodo(index)} title="Postpone Todo">
                    <FontAwesomeIcon icon={faClock} />
                  </button>
                </>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default App;