<template>
  <div>
    <p>{{ flaskData }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      flaskData: '' // Aquí se almacenará el mensaje de Flask
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/api/data')
        .then(response => {
          this.flaskData = response.data.data; // Asume que la respuesta es un objeto con una propiedad 'data'
        })
        .catch(error => {
          console.error("Hubo un error al obtener los datos de Flask:", error);
        });
    }
  }
}
</script>

