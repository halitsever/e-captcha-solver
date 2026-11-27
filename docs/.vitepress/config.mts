import { defineConfig } from 'vitepress'

const site = 'https://projects.halit.org/e-captcha-solver/'
const name = 'E-captcha solver'
const homeTitle = 'Captcha solver in Python: open-source CRNN-CTC OCR'
const description =
  'Open-source captcha OCR in Python. A PyTorch CRNN-CTC model that reads five-letter E-captcha text images, with training code, ONNX export and a FastAPI server.'

const repo = 'https://github.com/halitsever/e-captcha-solver'
const author = { '@type': 'Person', name: 'Halit Sever', url: 'https://github.com/halitsever' }

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareSourceCode',
  '@id': `${site}#source`,
  name,
  description,
  url: site,
  image: `${site}og.png`,
  codeRepository: repo,
  programmingLanguage: ['Python', 'JavaScript'],
  runtimePlatform: ['PyTorch', 'ONNX Runtime'],
  license: 'https://opensource.org/licenses/MIT',
  author,
}

export default defineConfig({
  /** keeps the page hash map out of every page's HTML, which Semrush reads as a low text-to-HTML ratio */
  metaChunk: true,
  base: '/e-captcha-solver/',
  lang: 'en',
  title: name,
  titleTemplate: `:title | ${name}`,
  description,
  cleanUrls: true,
  appearance: false,
  sitemap: { hostname: site },

  head: [
    /** Cloudflare Web Analytics, one token for every page on projects.halit.org. */
    ['script', { defer: '', src: 'https://static.cloudflareinsights.com/beacon.min.js', 'data-cf-beacon': '{"token": "dd7e54d3f48841c187d72d9dbb92a6b6"}' }],
    ['link', { rel: 'icon', href: '/e-captcha-solver/favicon.svg', type: 'image/svg+xml' }],
    ['link', { rel: 'icon', href: '/e-captcha-solver/favicon.png', type: 'image/png', sizes: '32x32' }],
    ['meta', { name: 'theme-color', content: '#a01020' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: name }],
    ['meta', { property: 'og:image', content: `${site}og.png` }],
    ['meta', { property: 'og:image:width', content: '1280' }],
    ['meta', { property: 'og:image:height', content: '640' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:image', content: `${site}og.png` }],
    ['script', { type: 'application/ld+json' }, JSON.stringify(jsonLd)],
  ],

  transformPageData(pageData) {
    const isHome = pageData.relativePath === 'index.md'
    const title = isHome ? homeTitle : `${pageData.frontmatter.title ?? pageData.title} | ${name}`
    const url = site + pageData.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '')
    const desc = pageData.frontmatter.description ?? description
    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push(
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:description', content: desc }],
      ['meta', { name: 'twitter:title', content: title }],
      ['meta', { name: 'twitter:description', content: desc }],
    )
  },

  markdown: {
    theme: 'github-light',
  },

  themeConfig: {
    logo: { src: '/logo.svg', alt: '' },
    siteTitle: name,
    nav: [
      { text: 'Quick start', link: '/guide/quick-start' },
      { text: 'The model', link: '/guide/crnn' },
      { text: 'CTC', link: '/guide/ctc-loss' },
      { text: 'Training', link: '/guide/training' },
    ],
    sidebar: [
      {
        text: 'Use it',
        items: [
          { text: 'Quick start', link: '/guide/quick-start' },
          { text: 'FastAPI server', link: '/guide/api-server' },
          { text: 'ONNX and Node.js', link: '/guide/onnx-node' },
        ],
      },
      {
        text: 'How it works',
        items: [
          { text: 'CRNN explained', link: '/guide/crnn' },
          { text: 'CTC loss and decoding', link: '/guide/ctc-loss' },
        ],
      },
      {
        text: 'Train it',
        items: [{ text: 'Training', link: '/guide/training' }],
      },
    ],
    outline: { level: 2, label: 'Sections' },
    socialLinks: [{ icon: 'github', link: repo }],
    search: { provider: 'local' },
    docFooter: { prev: 'Previous', next: 'Next' },
    footer: {
      message: 'MIT licence. Reads E-captcha text images only. Challenge widgets are out of scope.',
      copyright: 'Halit Sever',
    },
  },
})
