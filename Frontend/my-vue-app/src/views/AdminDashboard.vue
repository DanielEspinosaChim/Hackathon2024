<template>
    <div class="admin-dashboard">
        <h1>Hola {{ userName }}</h1>
      <div class="header">
        <button @click="toggleScheduleChange">Cambiar Horario</button>
      </div>
      <div class="current-schedule" v-if="showCurrentSchedule">
        <h2>Horario Actual</h2>
        <!-- Contenido del horario actual -->
      </div>
      <div class="schedule-change-modal" v-if="showModal">
        <div class="generator">
          <div class="subjects">
            <h2>Materias</h2>
            <select v-model="selectedSubject">
              <option disabled value="">Seleccione una materia</option>
              <option v-for="subject in subjectOptions" :key="subject" :value="subject">
                {{ subject }}
              </option>
            </select>
            <button @click="addSubject">Añadir Materia</button>
            <ul>
              <li v-for="(subject, index) in addedSubjects" :key="index">{{ subject }}</li>
            </ul>
          </div>
          <div class="classrooms">
            <h2>Aulas</h2>
            <select v-model="selectedClassroom">
              <option disabled value="">Seleccione un aula</option>
              <option v-for="classroom in classroomOptions" :key="classroom" :value="classroom">
                {{ classroom }}
              </option>
            </select>
            <button @click="addClassroom">Añadir Aula</button>
            <ul>
              <li v-for="(classroom, index) in addedClassrooms" :key="index">{{ classroom }}</li>
            </ul>
          </div>
          <button @click="generateSchedule">GENERAR</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        showModal: false,
        showCurrentSchedule: true,
        selectedSubject: '',
        subjectOptions: [],
        addedSubjects: [],
        selectedClassroom: '',
        classroomOptions: [],
        addedClassrooms: [],
      };
    },
    created() {
      this.fetchSubjects();
      this.fetchClassrooms();
    },
    computed: {
  userName() {
    const userName = localStorage.getItem('userName');
    console.log('Valor de userName en localStorage:', userName);
    return userName || 'Usuario';
  }
},
    methods: {
      toggleScheduleChange() {
        this.showModal = !this.showModal;
        this.showCurrentSchedule = !this.showCurrentSchedule;
      },
      fetchSubjects() {
        axios.get('http://localhost:5000/api/asignaturas') // Asegúrate de usar la URL completa.
          .then(response => {
            this.subjectOptions = response.data; // Asignación directa de la respuesta de la API
          })
          .catch(error => {
            console.error('Error al cargar las materias:', error);
          });
      },
      fetchClassrooms() {
        axios.get('http://localhost:5000/api/aulas') // Asegúrate de usar la URL completa.
          .then(response => {
            this.classroomOptions = response.data; // Asignación directa de la respuesta de la API
          })
          .catch(error => {
            console.error('Error al cargar las aulas:', error);
          });
      },
      addSubject() {
        if (this.selectedSubject && !this.addedSubjects.includes(this.selectedSubject)) {
          this.addedSubjects.push(this.selectedSubject);
          this.selectedSubject = ''; // Resetear el valor seleccionado
        }
      },
      addClassroom() {
        if (this.selectedClassroom && !this.addedClassrooms.includes(this.selectedClassroom)) {
          this.addedClassrooms.push(this.selectedClassroom);
          this.selectedClassroom = ''; // Resetear el valor seleccionado
        }
      },
      generateSchedule() {
        // Implementa aquí la lógica para manejar la generación del horario con las materias y aulas agregadas
        console.log('Materias agregadas:', this.addedSubjects);
        console.log('Aulas agregadas:', this.addedClassrooms);
        // Aquí podrías hacer una petición POST para enviar los datos al servidor y procesar el horario
      },
    }
  }
  </script>

  <style scoped>
  .admin-dashboard {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #4ecdc4;
    color: #333;
    padding: 20px;
  }
  
  .header button {
    padding: 10px;
    margin-bottom: 20px;
  }
  
  .current-schedule {
    background-color: white;
    border: 1px solid #ccc;
    padding: 20px;
  }
  
  .schedule-change-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 20px;
    border: 1px solid #ccc;
    z-index: 10;
  }
  
  .generator {
    display: flex;
    justify-content: space-between;
  }
  
  .subjects, .classrooms {
    margin: 10px;
    padding: 10px;
    border: 1px solid #ccc;
  }
  
  .subject, .classroom {
    margin-bottom: 5px;
  }
  select {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  font-size: 16px;
}

  
  button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #333;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #555;
}
  </style>
  