<template>
    <div class="teacher-dashboard">
      <h1>Hola Profe {{ userName }}</h1>
      <div class="toolbar">
        <!-- Iconos de toolbar aquí -->
      </div>
      <div class="nombramiento">
        <label for="nombramiento-input">Nombramiento:</label>
        <input type="number" id="nombramiento-input" v-model.number="nombramiento" min="4" max="40" @input="validateNombramiento">
      </div>
      <div class="availability">
        <h2>Horas disponibles</h2>
        <div class="calendar">
          <div class="days">
            <div>Lunes</div>
            <div>Martes</div>
            <div>Miércoles</div>
            <div>Jueves</div>
            <div>Viernes</div>
          </div>
          <div class="hours">
            <div v-for="hour in hours" :key="hour" class="hour-row">
              <div>{{ hour }}</div>
              <div class="hour-selection" v-for="day in days" :key="day"
                   :class="{'selected': isSelected(hour, day)}"
                   @click="toggleHour(day, hour)">
              </div>
            </div>
          </div>
        </div>
        <button @click="submitAvailability">Enviar</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Importa Axios para hacer solicitudes HTTP
  
  export default {
    name: 'TeacherDashboard',
    data() {
      return {
        nombramiento: null,
        hours: [
          '07:00 - 08:00 hrs', '08:00 - 09:00 hrs', '09:00 - 10:00 hrs',
          '10:00 - 11:00 hrs', '11:00 - 12:00 hrs', '12:00 - 13:00 hrs',
          '13:00 - 14:00 hrs', '14:00 - 15:00 hrs', '15:00 - 16:00 hrs',
          '16:00 - 17:00 hrs', '17:00 - 18:00 hrs', '18:00 - 19:00 hrs',
          '19:00 - 20:00 hrs', '20:00 - 21:00 hrs'
        ],
        days: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
        selectedHours: {}
      };
    },
    computed: {
      userName() {
        const userName = localStorage.getItem('userName');
        console.log('Valor de userName en localStorage:', userName);
        return userName || 'Usuario';
      }
    },
    methods: {
      validateNombramiento() {
        if (this.nombramiento < 4 || this.nombramiento > 40) {
          this.nombramiento = '';
        }
      },
      toggleHour(day, hour) {
        this.selectedHours[day] = this.selectedHours[day] || [];
        const index = this.selectedHours[day].indexOf(hour);
        if (index === -1) {
          this.selectedHours[day].push(hour);
        } else {
          this.selectedHours[day].splice(index, 1);
        }
      },
      isSelected(hour, day) {
        return this.selectedHours[day] && this.selectedHours[day].includes(hour);
      },
      async submitAvailability() {
  console.log('Horas seleccionadas:', this.selectedHours);
  console.log('Nombramiento:', this.nombramiento);

  // Format selected hours to HH:MM:SS format for backend compatibility
  const formattedHours = {};
  for (const day in this.selectedHours) {
    formattedHours[day] = this.selectedHours[day].map(hourRange => {
      const [start, end] = hourRange.split(' - ');
      const startTime = `${start}:00`; // Correctly formatted start time
      const endTime = `${end.split(' ')[0]}:00`; // Correctly formatted end time, removing 'hrs' and extra zeros
      return `${startTime} - ${endTime}`;
    });
  }

  // Construct data object to send to backend
  const data = {
    profesor_id: 1, // This should be dynamically set based on the actual teacher's ID
    disponibilidad: formattedHours,
    nombramiento: this.nombramiento
  };

  try {
    // Perform POST request to backend
    const response = await axios.post('http://localhost:5000/api/disponibilidad', data);

    // Log success message from backend
    console.log(response.data.message);
  } catch (error) {
    // Log any errors to the console
    console.error('Error al enviar disponibilidad:', error);
  }
}
    }
  }
  </script>
  
  <style scoped>
  .teacher-dashboard .toolbar {
    display: flex;
    justify-content: space-around;
    padding: 10px;
  }
  
  .teacher-dashboard .nombramiento {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px;
  }
  
  .teacher-dashboard .nombramiento input {
    margin-left: 5px;
    padding: 5px;
    border: 1px solid #ccc;
  }
  
  .teacher-dashboard .availability {
    margin: 10px;
  }
  
  .teacher-dashboard .calendar .days {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  text-align: center;
  font-weight: bold;
  }
  
  .teacher-dashboard .calendar .hours .hour-row {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr);
  margin-bottom: 5px;
  }
  .teacher-dashboard .calendar .hours .hour-selection {
    height: 20px; /* Altura reducida para los cuadros de selección */
    background-color: #f0f0f0;
    border: 1px solid #e0e0e0;
    cursor: pointer;
  }
  
  .teacher-dashboard .calendar .hours .hour-selection.selected {
    background-color: #4CAF50;
  }
  
  .teacher-dashboard .availability button {
    padding: 10px 20px;
    margin-top: 20px;
    background-color: #00BCD4;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>
  