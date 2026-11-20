import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { SITE } from '../config';
import { getIssues } from '../lib/issues';

export async function GET(context: APIContext) {
  const issues = await getIssues();
  return rss({
    title: SITE.name,
    description: `${SITE.tagline} ${SITE.description}`,
    site: context.site!,
    items: issues.map((issue) => ({
      title: issue.data.title,
      pubDate: issue.data.date,
      description: issue.data.summary,
      link: `/issues/${issue.id}/`,
      categories: [issue.data.sector, issue.data.company],
    })),
    customData: '<language>en-gb</language>',
  });
}
