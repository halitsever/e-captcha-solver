import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import '@fontsource-variable/newsreader/opsz.css'
import '@fontsource-variable/newsreader/opsz-italic.css'
import '@fontsource/ibm-plex-mono/400.css'
import '@fontsource/ibm-plex-mono/500.css'
import './style.css'
import Landing from './Landing.vue'
import SampleFigure from './SampleFigure.vue'
import ArchFigure from './ArchFigure.vue'
import CtcDecode from './CtcDecode.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Landing', Landing)
    app.component('SampleFigure', SampleFigure)
    app.component('ArchFigure', ArchFigure)
    app.component('CtcDecode', CtcDecode)
  },
} satisfies Theme
