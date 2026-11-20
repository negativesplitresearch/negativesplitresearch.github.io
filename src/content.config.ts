import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const issues = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/issues' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    company: z.string(),
    ticker: z.string().optional(),
    sector: z.string(),
    summary: z.string(),
    verdict: z.string().optional(),
    cover: z.string().optional(),
    /** Per-issue position disclosure, shown on the issue page. */
    disclosure: z.string().optional(),
    draft: z.boolean().default(true),
  }),
});

export const collections = { issues };
