/**
 * BRAIN OVERVIEW ROUTES — User Brain Page v3
 * 
 * Single aggregating endpoint for UI
 */

import { FastifyInstance } from 'fastify';
import { getBrainOverviewService } from './brain_overview.service.js';
import { getVersionInfo } from '../../core/version.js';

export async function brainOverviewRoutes(fastify: FastifyInstance): Promise<void> {
  const service = getBrainOverviewService();
  
  // Health check
  fastify.get('/api/ui/brain/health', async () => {
    return {
      ok: true,
      module: 'ui-brain',
      version: getVersionInfo(),
    };
  });
  
  // Main aggregating endpoint
  fastify.get<{ Querystring: { asOf?: string } }>(
    '/api/ui/brain/overview',
    async (req, reply) => {
      try {
        const { asOf } = req.query;
        const pack = await service.getOverview(asOf);
        
        return {
          ok: true,
          ...pack,
        };
      } catch (err) {
        reply.code(500);
        return {
          ok: false,
          error: (err as Error).message,
        };
      }
    }
  );
  
  fastify.log.info('[UI Brain] Routes registered at /api/ui/brain/*');
}

export default brainOverviewRoutes;
