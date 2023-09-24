<template>
  <div class="flex h-screen bg-gray-100">
    <div class="w-1/2 p-6 bg-white rounded-r-lg shadow-md">
      <h2 class="mb-6 text-2xl font-semibold text-gray-700">Select a Template</h2>
      <div class="mb-6">
        <select v-model="selectedTemplate" @change="loadTemplate" class="w-full p-4 bg-gray-200 border rounded-lg shadow-sm focus:outline-none focus:border-blue-300">
          <option v-for="template in templates" :key="template" :value="template">
            {{ template }}
          </option>
        </select>
      </div>

      <h2 class="mb-6 text-2xl font-semibold text-gray-700">Input Values</h2>
      <div v-for="(value, key) in params" :key="key" class="mb-6">
        <label class="block mb-2 text-lg font-medium text-gray-600">{{ key }}</label>
        <textarea 
            v-model="params[key]" 
            @input="renderMarkdown" 
            class="w-full h-16 p-4 bg-gray-200 border rounded-lg shadow-sm focus:outline-none focus:border-blue-300 resize-none">
        </textarea>
      </div>
    </div>

    <div class="w-1/2 p-6 bg-white rounded-l-lg shadow-md">
      <h2 class="mb-6 text-2xl font-semibold text-gray-700">Preview: Rendered Markdown</h2>
      <div class="prose max-w-full mb-8 overflow-y-auto h-[38vh] bg-gray-100 border rounded-lg p-4 shadow-inner" v-html="processedMarkdown"></div>
      
      <h2 class="mb-6 text-2xl font-semibold text-gray-700">Raw Markdown Content</h2>
      <textarea readonly class="w-full h-[38vh] p-4 bg-gray-200 border rounded-lg shadow-sm overflow-y-auto resize-none" v-text="rawMarkdown"></textarea>

      <button @click="copyMarkdown" class="p-3 w-full mt-6 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300 ease-in-out">Copy Markdown to Clipboard</button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { marked } from 'marked';

export default {
  data() {
    return {
      templates: [],
      selectedTemplate: null,
      rawTemplate: '',
      params: {},
      processedMarkdown: '',
      rawMarkdown: ''
    };
  },
  mounted() {
    axios.get('http://localhost:8000/templates/').then(response => {
      this.templates = response.data.list;
      if (this.templates.length > 0) {
        this.selectedTemplate = this.templates[0];
        this.loadTemplate();
      }
    });
  },
  methods: {
    copyMarkdown() {
  navigator.clipboard.writeText(this.rawMarkdown).then(function() {
    alert("Markdown copied to clipboard!");
  }).catch(function(err) {
    console.error("Could not copy markdown: ", err);
    alert("Could not copy markdown. Please try again.");
  });
},

    loadTemplate() {
  axios.get(`http://localhost:8000/template/${this.selectedTemplate}`).then(response => {
    this.rawTemplate = response.data.data;
    this.params = {};  // Reset params here
    this.parseParams();
    this.renderMarkdown();
  });
},
parseParams() {
  const matches = [...this.rawTemplate.matchAll(/\{\{(.+?)\}\}/g)];
  for (let match of matches) {
    this.params[match[1]] = this.params[match[1]] || ''; 
  }

    },
    renderMarkdown() {
  axios.post("http://localhost:8000/process_markdown/", {
    template_name: this.selectedTemplate,
    params: this.params
  }).then(response => {
    this.rawMarkdown = response.data.markdown;  
    this.processedMarkdown = marked(this.rawMarkdown);  
  });
}

  }
};
</script>
