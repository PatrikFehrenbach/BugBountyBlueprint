<template>
  <div class="p-4 max-w-screen-lg mx-auto">
      <h1 class="mb-4 text-2xl font-bold">Available Templates</h1>
      <ul class="mb-6">
          <li v-for="template in templates" :key="template" class="mb-2 p-2 bg-gray-200 rounded shadow-md flex items-center justify-between">
              <span class="font-medium">{{ template }}</span>
              <div>
                  <button @click="loadTemplate(template)" class="ml-2 px-4 py-1 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition duration-300">Edit</button>
                  <button @click="deleteTemplate(template)" class="ml-2 px-4 py-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition duration-300">Delete</button>
              </div>
          </li>
      </ul>

      <h1 class="mb-4 text-2xl font-bold">Edit Template</h1>
      <div class="p-6 border rounded-lg shadow-lg">
          <input v-model="currentTemplateName" placeholder="Enter template name (e.g. my_template.md)" class="block w-full p-3 mb-4 border rounded-lg shadow-sm focus:outline-none focus:border-blue-300" />
          <textarea v-model="currentTemplateContent" placeholder="Enter markdown content here..." class="block w-full h-48 p-3 mb-4 border rounded-lg shadow-sm focus:outline-none focus:border-blue-300 resize-none"></textarea>
          <button @click="saveTemplate" class="p-3 w-full bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300">Save Changes</button>
      </div>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        templates: [],
        currentTemplateName: '',
        currentTemplateContent: ''
      };
    },
    mounted() {
      this.fetchTemplates();
    },
    methods: {
      fetchTemplates() {
        axios.get('http://localhost:8000/templates/')
          .then(response => {
            this.templates = response.data.list;
          });
      },
      loadTemplate(name) {
        axios.get(`http://localhost:8000/template/${name}`)
          .then(response => {
            this.currentTemplateName = name;
            this.currentTemplateContent = response.data.data;
          });
      },
      deleteTemplate(name) {
        axios.delete(`http://localhost:8000/template/${name}`)
          .then(() => {
            this.fetchTemplates();
            alert("Template deleted successfully");
          });
      },
      saveTemplate() {
  const templateData = {
    name: this.currentTemplateName,
    content: this.currentTemplateContent
  };

  const method = this.templates.includes(this.currentTemplateName) ? 'put' : 'post';
  const url = method === 'put'
    ? `http://localhost:8000/template/${this.currentTemplateName}`
    : 'http://localhost:8000/template/';

  axios[method](url, templateData)
    .then(() => {
      this.fetchTemplates();
      alert("Template saved successfully");
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Error saving template. Please check the console for details.");
    });
      }
    }
  };
  </script>
  