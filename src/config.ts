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

/**
 * Upcoming topics shown on the homepage ("On the start line").
 * Editorial plan, not promises: edit freely, and remove an entry once its issue is published.
 */
export const UPCOMING: { company: string; sector: string; question: string }[] = [
  { company: 'Garmin', sector: 'Wearables', question: 'From GPS watches to a training platform: where the money now comes from' },
  { company: 'On Holding', sector: 'Running shoes', question: 'Growing faster than the category, and what that growth costs' },
  { company: 'Strava', sector: 'Fitness apps', question: 'The economics of a subscription social network for athletes' },
  { company: 'IRONMAN Group', sector: 'Events', question: 'What a race series is worth, and who captures the entry fee' },
];
