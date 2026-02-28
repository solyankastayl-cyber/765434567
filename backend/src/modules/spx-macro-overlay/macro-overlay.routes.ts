/**
 * SPX MACRO OVERLAY ROUTES
 * 
 * Provides SPX projections with DXY macro adjustment
 * 
 * GET /api/spx/macro-overlay?horizon=30d
 * Returns: adjusted projection + base hybrid + DXY macro influence
 */

import type { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { buildMacroOverlaySPX, type ProjectionPack } from './macro-overlay.engine.js';

const API_BASE = 'http://localhost:8002';

// ═══════════════════════════════════════════════════════════════
// FETCH HELPERS
// ═══════════════════════════════════════════════════════════════

async function fetchSPXHybrid(horizon: string): Promise<ProjectionPack | null> {
  try {
    const response = await fetch(`${API_BASE}/api/fractal/spx?focus=${horizon}`);
    if (!response.ok) return null;
    
    const data = await response.json();
    if (!data.ok) return null;
    
    // Transform to ProjectionPack
    const stats = data.overlay?.stats || {};
    const hybridPath = data.projection?.hybrid?.path || [];
    
    return {
      horizon,
      asOf: data.meta?.asOf || new Date().toISOString(),
      expectedP50: (stats.medianReturn || 0) * 100,
      rangeP10P90: [
        (stats.p10Return || -0.05) * 100,
        (stats.p90Return || 0.05) * 100,
      ],
      series: hybridPath.map((p: any) => ({ t: p.d || p.t, y: p.v || p.y })),
      confidence: stats.hitRate || 0.5,
      quality: data.diagnostics?.qualityScore ? data.diagnostics.qualityScore * 100 : 50,
      dataStatus: data.meta?.dataStatus || 'REAL',
    };
  } catch (e) {
    console.error('[SPX Macro Overlay] Failed to fetch SPX hybrid:', e);
    return null;
  }
}

async function fetchDXYMacro(horizon: string): Promise<ProjectionPack | null> {
  try {
    const horizonDays = parseInt(horizon) || 30;
    const response = await fetch(`${API_BASE}/api/ui/fractal/dxy/overview?h=${horizonDays}`);
    if (!response.ok) return null;
    
    const data = await response.json();
    if (!data.ok) return null;
    
    // Get macro-adjusted values from DXY
    const verdict = data.verdict || {};
    const chart = data.chart || {};
    const macro = data.macro || {};
    
    return {
      horizon,
      asOf: data.generatedAt || new Date().toISOString(),
      expectedP50: verdict.expectedMoveP50 || 0,
      rangeP10P90: [verdict.rangeP10 || -5, verdict.rangeP90 || 5],
      series: (chart.macroPath || chart.hybridPath || []).map((p: any) => ({
        t: p.t || p.date,
        y: p.y || p.value,
      })),
      confidence: (verdict.confidence || 50) / 100,
      quality: macro.confidence || 50,
      dataStatus: data.header?.dataStatus || 'REAL',
    };
  } catch (e) {
    console.error('[SPX Macro Overlay] Failed to fetch DXY macro:', e);
    return null;
  }
}

// ═══════════════════════════════════════════════════════════════
// ROUTES
// ═══════════════════════════════════════════════════════════════

export default async function spxMacroOverlayRoutes(fastify: FastifyInstance) {
  // GET /api/spx/macro-overlay
  fastify.get('/api/spx/macro-overlay', async (request: FastifyRequest, reply: FastifyReply) => {
    const { horizon = '30d' } = request.query as { horizon?: string };
    
    try {
      // Fetch both data sources in parallel
      const [spxHybrid, dxyMacro] = await Promise.all([
        fetchSPXHybrid(horizon),
        fetchDXYMacro(horizon),
      ]);
      
      if (!spxHybrid) {
        return reply.status(500).send({
          ok: false,
          error: 'Failed to fetch SPX hybrid data',
        });
      }
      
      if (!dxyMacro) {
        // Return SPX without overlay if DXY unavailable
        return reply.send({
          ok: true,
          mode: 'hybrid_only',
          adjusted: spxHybrid,
          baseHybrid: spxHybrid,
          dxyMacro: null,
          meta: {
            overlayActive: false,
            reasonCodes: ['DXY_UNAVAILABLE'],
          },
        });
      }
      
      // Build macro overlay
      const result = buildMacroOverlaySPX(spxHybrid, dxyMacro);
      
      return reply.send({
        ok: true,
        mode: 'macro',
        ...result,
        horizon,
        generatedAt: new Date().toISOString(),
      });
    } catch (e) {
      console.error('[SPX Macro Overlay] Error:', e);
      return reply.status(500).send({
        ok: false,
        error: 'Internal error building macro overlay',
      });
    }
  });
  
  // GET /api/spx/macro-overlay/calibration
  fastify.get('/api/spx/macro-overlay/calibration', async (request: FastifyRequest, reply: FastifyReply) => {
    const { BETA_BY_HORIZON, CORR_BY_HORIZON, DEFAULT_CALIBRATION } = await import('./macro-overlay.engine.js');
    
    return reply.send({
      ok: true,
      beta: BETA_BY_HORIZON,
      corr: CORR_BY_HORIZON,
      calibration: DEFAULT_CALIBRATION,
    });
  });
  
  console.log('[Fractal] ✅ SPX Macro Overlay routes registered at /api/spx/macro-overlay/*');
}
