import { createRouter, createWebHistory } from 'vue-router';
import MarkdownEditor from './components/MarkDownEditor.vue';
import TemplateManager from './components/TemplateManager.vue';

const routes = [
  {
    path: '/',
    name: 'editor',
    component: MarkdownEditor,
  },
  {
    path: '/templates',
    name: 'templates',
    component: TemplateManager,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
