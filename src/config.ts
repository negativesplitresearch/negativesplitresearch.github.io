export const SITE = {
  name: 'Negative Split Research',
  tagline: 'The business behind the finish line.',
  description:
    'Independent analysis of the business of endurance sports: the companies, deals and economics behind running, triathlon, cycling and swimming.',
  url: 'https://negativesplitresearch.github.io',
  ogImage: '/og-default.png',
  disclaimerShort: 'Not investment advice. For information and education only.',
};

/**
 * Beehiiv signup embed. Rendered verbatim via `set:html` in <Signup />,
 * so Astro never bundles, hoists or strips the script tag.
 */
export const BEEHIIV_EMBED = `<script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="22d6c51c-cd5c-4130-b389-a322f0629f33"></script>`;

export const NAV = [
  { href: '/issues/', label: 'Issues' },
  { href: '/about/', label: 'About' },
];
