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

/** BlogPosting, breadcrumbs and, when the post shows an FAQ, FAQPage data for a blog post. */
function postJsonLd(fm: Record<string, any>, url: string, desc: string) {
  const graph: object[] = [
    {
      '@type': 'BlogPosting',
      headline: fm.headline ?? fm.title,
      description: desc,
      url,
      mainEntityOfPage: url,
      datePublished: fm.date,
      dateModified: fm.date,
      inLanguage: fm.lang ?? 'en',
      image: `${site}og.png`,
      keywords: fm.keyword,
      author: { ...author, url: 'https://halit.org' },
      publisher: { ...author, url: 'https://halit.org' },
    },
    {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name, item: site },
        { '@type': 'ListItem', position: 2, name: 'Blog', item: `${site}blog/` },
        { '@type': 'ListItem', position: 3, name: fm.headline ?? fm.title, item: url },
      ],
    },
  ]
  if (fm.faq?.length) {
    graph.push({
      '@type': 'FAQPage',
      mainEntity: fm.faq.map((f: { q: string; a: string }) => ({
        '@type': 'Question',
        name: f.q,
        acceptedAnswer: { '@type': 'Answer', text: f.a.replace(/<[^>]+>|`/g, '') },
      })),
    })
  }
  return { '@context': 'https://schema.org', '@graph': graph }
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
    ['meta', { property: 'og:site_name', content: name }],
    ['meta', { property: 'og:image', content: `${site}og.png` }],
    ['meta', { property: 'og:image:width', content: '1280' }],
    ['meta', { property: 'og:image:height', content: '640' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:image', content: `${site}og.png` }],
    ['script', { type: 'application/ld+json' }, JSON.stringify(jsonLd)],
  ],

  transformPageData(pageData) {
    const fm = pageData.frontmatter
    const isHome = pageData.relativePath === 'index.md'
    const ownTitle = isHome || fm.titleTemplate === false
    const title = isHome ? homeTitle : ownTitle ? fm.title : `${fm.title ?? pageData.title} | ${name}`
    const url = site + pageData.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '')
    const desc = fm.description ?? description
    fm.head ??= []
    fm.head.push(['meta', { property: 'og:type', content: fm.date ? 'article' : 'website' }])
    if (fm.date) fm.head.push(['script', { type: 'application/ld+json' }, JSON.stringify(postJsonLd(fm, url, desc))])
    for (const [lang, path] of Object.entries(fm.hreflang ?? {})) {
      fm.head.push(['link', { rel: 'alternate', hreflang: lang, href: site + path }])
    }
    fm.head.push(
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:description', content: desc }],
      ['meta', { name: 'twitter:title', content: title }],
      ['meta', { name: 'twitter:description', content: desc }],
    )
  },

  /** Posts in another language set `lang` in frontmatter; VitePress only knows the site language. */
  transformHtml(code, _id, { pageData }) {
    const lang = pageData.frontmatter.lang
    return lang ? code.replace('<html lang="en"', `<html lang="${lang}"`) : code
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
      { text: 'Blog', link: '/blog/' },
    ],
    sidebar: {
      '/blog/': [
        {
          text: 'Blog',
          items: [
            { text: 'All posts', link: '/blog/' },
            { text: 'What is a CAPTCHA?', link: '/blog/what-is-a-captcha-challenge' },
            { text: 'Math CAPTCHAs', link: '/blog/mathematical-captcha' },
            { text: 'What is a captcha code?', link: '/blog/what-is-a-captcha-code' },
            { text: 'Google unusual traffic', link: '/blog/google-captcha-unusual-traffic' },
            { text: 'How captcha OCR works', link: '/blog/how-captcha-ocr-works' },
            { text: 'Python OCR', link: '/blog/python-ocr-image-to-text' },
            { text: 'Tesseract vs CRNN', link: '/blog/tesseract-vs-crnn-captcha' },
            { text: 'Captcha ne demek?', link: '/blog/captcha-ne-demek' },
          ],
        },
      ],
      '/': [
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
    },
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
