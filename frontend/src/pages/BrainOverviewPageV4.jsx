/**
 * BRAIN v4 — DECISION ENGINE PAGE
 * 
 * Brain is not a dashboard. It's a decision engine.
 * It answers: Where are we? What to do? Why? How confident?
 * 
 * Structure:
 * Layer 1: Final Verdict (The Answer)
 * Layer 2: Why This View (Reasoning)
 * Layer 3: Horizon Phase Map
 * Layer 4: Risk Map
 * Layer 5: Causal Flow
 * Layer 6: Macro Indicators (detail)
 * Layer 7: Allocation Pipeline
 * Layer 8: Capital Scaling
 * Layer 9: Model Transparency
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Brain, 
  Shield, 
  TrendingUp, 
  TrendingDown,
  Minus,
  AlertTriangle,
  CheckCircle,
  Activity,
  ArrowRight,
  ChevronDown,
  ChevronUp,
  Info,
  Zap,
  Target,
  Scale,
  BarChart3,
  Clock,
  Layers
} from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

// ═══════════════════════════════════════════════════════════════
// COLORS & HELPERS
// ═══════════════════════════════════════════════════════════════

const getSentimentColor = (sentiment) => {
  switch (sentiment) {
    case 'supportive': return 'text-emerald-600';
    case 'risk': return 'text-red-600';
    default: return 'text-amber-600';
  }
};

const getSentimentBg = (sentiment) => {
  switch (sentiment) {
    case 'supportive': return 'bg-emerald-50';
    case 'risk': return 'bg-red-50';
    default: return 'bg-amber-50';
  }
};

const getSentimentDot = (sentiment) => {
  switch (sentiment) {
    case 'supportive': return 'bg-emerald-500';
    case 'risk': return 'bg-red-500';
    default: return 'bg-amber-500';
  }
};

const getPostureStyles = (posture) => {
  switch (posture) {
    case 'OFFENSIVE': return { bg: 'bg-emerald-100', text: 'text-emerald-800', border: 'border-emerald-200' };
    case 'DEFENSIVE': return { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-200' };
    default: return { bg: 'bg-gray-100', text: 'text-gray-800', border: 'border-gray-200' };
  }
};

const getBiasStyles = (bias) => {
  switch (bias) {
    case 'BULLISH': return { text: 'text-emerald-700', icon: TrendingUp };
    case 'BEARISH': return { text: 'text-red-700', icon: TrendingDown };
    default: return { text: 'text-gray-700', icon: Minus };
  }
};

const getPhaseColor = (phase) => {
  switch (phase) {
    case 'BULLISH': return 'text-emerald-600 bg-emerald-50';
    case 'BEARISH': return 'text-red-600 bg-red-50';
    default: return 'text-gray-600 bg-gray-50';
  }
};

const getStrengthWidth = (strength) => {
  switch (strength) {
    case 'strong': return 'w-full';
    case 'medium': return 'w-2/3';
    default: return 'w-1/3';
  }
};

const getCausalColor = (direction) => {
  switch (direction) {
    case 'positive': return '#10B981'; // emerald
    case 'negative': return '#EF4444'; // red
    default: return '#9CA3AF'; // gray
  }
};

// ═══════════════════════════════════════════════════════════════
// TOOLTIP COMPONENT
// ═══════════════════════════════════════════════════════════════

const Tooltip = ({ children, content }) => {
  const [show, setShow] = useState(false);
  
  if (!content) return children;
  
  return (
    <div className="relative inline-block" onMouseEnter={() => setShow(true)} onMouseLeave={() => setShow(false)}>
      {children}
      {show && (
        <div className="absolute z-50 w-72 p-3 text-xs bg-white border border-gray-100 rounded-lg shadow-lg -top-2 left-full ml-2">
          {content}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 1: FINAL VERDICT
// ═══════════════════════════════════════════════════════════════

const VerdictBlock = ({ verdict, action }) => {
  if (!verdict || !action) return null;
  
  const postureStyles = getPostureStyles(verdict.posture);
  const biasStyles = getBiasStyles(verdict.dominantBias);
  const BiasIcon = biasStyles.icon;
  
  return (
    <div className="mb-8">
      {/* Main Verdict Card */}
      <div className="bg-white rounded-xl p-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900 mb-1">Market Verdict</h1>
            <p className="text-sm text-gray-500">Decision engine output</p>
          </div>
          <div className={`px-4 py-2 rounded-full ${postureStyles.bg} ${postureStyles.text} font-medium text-sm`}>
            {verdict.posture}
          </div>
        </div>
        
        {/* Verdict Grid */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Regime</p>
            <p className="text-lg font-medium text-gray-900">{verdict.regime?.replace('_', ' ')}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Dominant Bias (90D)</p>
            <div className={`flex items-center gap-2 ${biasStyles.text}`}>
              <BiasIcon className="w-5 h-5" />
              <span className="text-lg font-medium">{verdict.dominantBias}</span>
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Posture</p>
            <p className="text-lg font-medium text-gray-900">{verdict.posture}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Confidence</p>
            <p className="text-lg font-medium text-gray-900">{verdict.confidence}%</p>
          </div>
        </div>
        
        {/* Primary Action - Big and Clear */}
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Primary Action</p>
          <p className="text-xl font-medium text-gray-900">{action.primary}</p>
        </div>
        
        {/* Size Guidance */}
        <div className="grid grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Size Multiplier</p>
            <p className="text-2xl font-semibold text-gray-900">{action.multiplier}x</p>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Cash Buffer</p>
            <p className="text-2xl font-semibold text-gray-900">{action.cashBufferRange}</p>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Leverage</p>
            <p className="text-2xl font-semibold text-gray-900">{action.leverageRecommended ? 'Yes' : 'No'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 2: WHY THIS VIEW
// ═══════════════════════════════════════════════════════════════

const ReasonsBlock = ({ reasons }) => {
  if (!reasons || reasons.length === 0) return null;
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Why This View</h2>
      <div className="space-y-3">
        {reasons.map((reason, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <div className={`w-2 h-2 rounded-full ${getSentimentDot(reason.sentiment)}`} />
            <span className={`text-sm ${getSentimentColor(reason.sentiment)}`}>
              {reason.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 3: HORIZON PHASE MAP
// ═══════════════════════════════════════════════════════════════

const HorizonBlock = ({ horizons }) => {
  if (!horizons || horizons.length === 0) return null;
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Market Phase by Horizon</h2>
        <Tooltip content="Phase derived from combined fractal + macro regime model">
          <Info className="w-4 h-4 text-gray-400 cursor-help" />
        </Tooltip>
      </div>
      
      <div className="grid grid-cols-4 gap-4">
        {horizons.map((h) => (
          <div key={h.horizon} className="text-center">
            <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">{h.horizon}D</p>
            <div className={`py-3 px-4 rounded-lg ${getPhaseColor(h.phase)}`}>
              <p className="font-medium">{h.phase}</p>
              <p className="text-xs mt-1 opacity-70 capitalize">{h.strength}</p>
            </div>
            {/* Strength bar */}
            <div className="mt-2 h-1 bg-gray-100 rounded-full overflow-hidden">
              <div className={`h-full bg-current ${getStrengthWidth(h.strength)} ${getPhaseColor(h.phase).split(' ')[0]}`} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 4: RISK MAP
// ═══════════════════════════════════════════════════════════════

const RiskBlock = ({ risk }) => {
  if (!risk) return null;
  
  const isElevated = risk.guardStatus !== 'none' || risk.volatilityRegime === 'elevated' || risk.volatilityRegime === 'extreme';
  
  return (
    <div className={`rounded-xl p-6 mb-8 ${isElevated ? 'bg-red-50' : 'bg-white'}`}>
      <div className="flex items-center gap-2 mb-4">
        <Shield className={`w-5 h-5 ${isElevated ? 'text-red-600' : 'text-gray-600'}`} />
        <h2 className={`text-lg font-semibold ${isElevated ? 'text-red-900' : 'text-gray-900'}`}>Risk Map</h2>
      </div>
      
      <div className="grid grid-cols-5 gap-4">
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Volatility</p>
          <p className="font-medium text-gray-900 capitalize">{risk.volatilityRegime}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Tail Risk</p>
          <p className="font-medium text-gray-900 capitalize">{risk.tailRisk}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Guard Status</p>
          <p className={`font-medium capitalize ${risk.guardStatus !== 'none' ? 'text-red-600' : 'text-gray-900'}`}>
            {risk.guardStatus}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Override</p>
          <p className="font-medium text-gray-900">{risk.overrideIntensity}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Capital Scale</p>
          <p className="font-medium text-gray-900">{risk.capitalScaling}%</p>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 5: CAUSAL FLOW
// ═══════════════════════════════════════════════════════════════

const CausalBlock = ({ causal }) => {
  if (!causal || causal.length === 0) return null;
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Causal Flow</h2>
      
      <div className="space-y-4">
        {causal.map((chain) => (
          <div key={chain.id} className="flex items-center gap-2 flex-wrap">
            {chain.links.map((link, idx) => (
              <React.Fragment key={idx}>
                <span className="text-sm font-medium text-gray-700">{link.from}</span>
                <ArrowRight 
                  className="w-4 h-4" 
                  style={{ color: getCausalColor(link.direction) }}
                />
                {idx === chain.links.length - 1 && (
                  <span className="text-sm font-medium text-gray-700">{link.to}</span>
                )}
              </React.Fragment>
            ))}
            <span className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
              chain.netEffect === 'positive' ? 'bg-emerald-100 text-emerald-700' :
              chain.netEffect === 'negative' ? 'bg-red-100 text-red-700' :
              'bg-gray-100 text-gray-700'
            }`}>
              {chain.targetAsset}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 6: MACRO INDICATORS
// ═══════════════════════════════════════════════════════════════

const MacroIndicatorCard = ({ indicator }) => {
  const tooltipContent = (
    <div className="space-y-2">
      <p><strong>Current:</strong> {indicator.currentValue}</p>
      <p><strong>Normal Range:</strong> {indicator.normalRange}</p>
      <p><strong>Risk Zone:</strong> {indicator.riskRange}</p>
      <hr className="border-gray-100" />
      <p><strong>Bullish when:</strong> {indicator.bullishCondition}</p>
      <p><strong>Bearish when:</strong> {indicator.bearishCondition}</p>
      <hr className="border-gray-100" />
      <p><strong>USD Impact:</strong> {indicator.usdImpact}</p>
      <p><strong>SPX Impact:</strong> {indicator.spxImpact}</p>
      <p><strong>BTC Impact:</strong> {indicator.btcImpact}</p>
    </div>
  );
  
  return (
    <Tooltip content={tooltipContent}>
      <div className={`p-4 rounded-lg cursor-help ${getSentimentBg(indicator.status)}`}>
        <div className="flex items-start justify-between mb-2">
          <p className="text-xs text-gray-500">{indicator.title}</p>
          <Info className="w-3 h-3 text-gray-400" />
        </div>
        <p className={`text-xl font-semibold ${getSentimentColor(indicator.status)}`}>
          {indicator.currentValue}
        </p>
        <p className="text-xs text-gray-500 mt-1">{indicator.interpretation}</p>
      </div>
    </Tooltip>
  );
};

const MacroBlock = ({ macroSummary }) => {
  if (!macroSummary || macroSummary.length === 0) return null;
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Macro Indicators</h2>
      <div className="grid grid-cols-3 gap-4">
        {macroSummary.map((indicator) => (
          <MacroIndicatorCard key={indicator.key} indicator={indicator} />
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 7: ALLOCATION PIPELINE
// ═══════════════════════════════════════════════════════════════

const AllocationBlock = ({ allocation }) => {
  if (!allocation) return null;
  
  const steps = [
    { label: 'Base', data: allocation.base },
    { label: 'After Brain', data: allocation.afterBrain },
    { label: 'Final', data: allocation.final },
  ];
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Allocation Pipeline</h2>
      
      {/* Pipeline visualization */}
      <div className="flex items-center justify-between mb-6">
        {steps.map((step, idx) => (
          <React.Fragment key={step.label}>
            <div className="flex-1 text-center">
              <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">{step.label}</p>
              <div className="flex justify-center gap-4">
                <div>
                  <p className="text-xs text-gray-400">SPX</p>
                  <p className="font-medium text-gray-900">{step.data.spx}%</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">BTC</p>
                  <p className="font-medium text-gray-900">{step.data.btc}%</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Cash</p>
                  <p className="font-medium text-gray-900">{step.data.cash}%</p>
                </div>
              </div>
            </div>
            {idx < steps.length - 1 && (
              <ArrowRight className="w-5 h-5 text-gray-300 mx-2" />
            )}
          </React.Fragment>
        ))}
      </div>
      
      {/* Impact breakdown */}
      <div className="grid grid-cols-4 gap-4 pt-4 border-t border-gray-100">
        <div>
          <p className="text-xs text-gray-400">Brain Impact</p>
          <p className="font-medium text-gray-900">{allocation.impact.brainImpact > 0 ? '+' : ''}{allocation.impact.brainImpact}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Optimizer Impact</p>
          <p className="font-medium text-gray-900">{allocation.impact.optimizerImpact > 0 ? '+' : ''}{allocation.impact.optimizerImpact}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Scaling Impact</p>
          <p className="font-medium text-gray-900">{allocation.impact.scalingImpact > 0 ? '+' : ''}{allocation.impact.scalingImpact}%</p>
        </div>
        <div className="col-span-1">
          <p className="text-xs text-gray-400">Status</p>
          <p className="text-sm text-gray-600">{allocation.impact.explanation}</p>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 8: CAPITAL SCALING
// ═══════════════════════════════════════════════════════════════

const CapitalScalingBlock = ({ capitalScaling }) => {
  if (!capitalScaling) return null;
  
  return (
    <div className="bg-white rounded-xl p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Capital Scaling</h2>
        <span className="text-2xl font-bold text-gray-900">{capitalScaling.scaleFactor}%</span>
      </div>
      
      {/* Drivers */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        {capitalScaling.drivers.map((driver) => (
          <div key={driver.name} className="p-3 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-400">{driver.name}</p>
            <p className={`font-medium ${
              driver.effect === 'reduce' ? 'text-amber-600' : 'text-gray-900'
            }`}>{driver.value}%</p>
          </div>
        ))}
      </div>
      
      <p className="text-sm text-gray-600">{capitalScaling.explanation}</p>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// LAYER 9: MODEL TRANSPARENCY
// ═══════════════════════════════════════════════════════════════

const TransparencyBlock = ({ transparency }) => {
  if (!transparency) return null;
  
  return (
    <div className="bg-gray-50 rounded-xl p-6 mb-8">
      <h2 className="text-sm font-medium text-gray-500 mb-3">Model Transparency</h2>
      <div className="flex items-center gap-8 text-xs text-gray-500">
        <span>Version: {transparency.systemVersion}</span>
        <span>Capital Scaling: {transparency.capitalScalingVersion}</span>
        <span>Data: {transparency.dataAsOf}</span>
        <span>Hash: {transparency.determinismHash}</span>
        {transparency.frozen && <span className="text-amber-600">FROZEN</span>}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// ADVANCED DECOMPOSITION (hidden by default)
// ═══════════════════════════════════════════════════════════════

const AdvancedBlock = ({ advanced }) => {
  const [expanded, setExpanded] = useState(false);
  
  if (!advanced) return null;
  
  return (
    <div className="bg-white rounded-xl p-6">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="flex items-center justify-between w-full text-left"
      >
        <h2 className="text-sm font-medium text-gray-500">Model Decomposition (Advanced)</h2>
        {expanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
      </button>
      
      {expanded && (
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-gray-400 uppercase">
                <th className="text-left py-2">Horizon</th>
                <th className="text-right py-2">Baseline</th>
                <th className="text-right py-2">Replay</th>
                <th className="text-right py-2">Combined</th>
                <th className="text-right py-2">Macro Adj</th>
                <th className="text-right py-2">Delta</th>
              </tr>
            </thead>
            <tbody>
              {advanced.horizons.map((h) => (
                <tr key={h.horizon} className="border-t border-gray-100">
                  <td className="py-2 font-medium">{h.horizon}D</td>
                  <td className="text-right py-2">{h.synthetic > 0 ? '+' : ''}{h.synthetic}%</td>
                  <td className="text-right py-2">{h.replay > 0 ? '+' : ''}{h.replay}%</td>
                  <td className="text-right py-2">{h.hybrid > 0 ? '+' : ''}{h.hybrid}%</td>
                  <td className="text-right py-2">{h.macroAdj > 0 ? '+' : ''}{h.macroAdj}%</td>
                  <td className="text-right py-2 text-gray-400">{h.macroDelta > 0 ? '+' : ''}{h.macroDelta}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
// MAIN PAGE COMPONENT
// ═══════════════════════════════════════════════════════════════

const BrainOverviewPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/ui/brain/decision`);
      const result = await response.json();
      
      if (result.ok) {
        setData(result);
        setError(null);
      } else {
        setError(result.error || 'Failed to fetch data');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Brain className="w-12 h-12 text-gray-300 mx-auto mb-4 animate-pulse" />
          <p className="text-gray-500">Loading Brain Overview...</p>
          <p className="text-xs text-gray-400 mt-1">This may take up to 15 seconds</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p className="text-red-600">Error loading data</p>
          <p className="text-sm text-gray-500 mt-1">{error}</p>
          <button 
            onClick={fetchData}
            className="mt-4 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }
  
  if (!data) return null;
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Brain Overview</h1>
          <p className="text-gray-500 mt-1">Institutional AI Macro Risk Dashboard</p>
        </div>
        
        {/* Layer 1: Verdict */}
        <VerdictBlock verdict={data.verdict} action={data.action} />
        
        {/* Layer 2: Reasons */}
        <ReasonsBlock reasons={data.reasons} />
        
        {/* Layer 3: Horizons */}
        <HorizonBlock horizons={data.horizons} />
        
        {/* Layer 4: Risk */}
        <RiskBlock risk={data.risk} />
        
        {/* Layer 5: Causal Flow */}
        <CausalBlock causal={data.causal} />
        
        {/* Layer 6: Macro Indicators */}
        <MacroBlock macroSummary={data.macroSummary} />
        
        {/* Layer 7: Allocation */}
        <AllocationBlock allocation={data.allocation} />
        
        {/* Layer 8: Capital Scaling */}
        <CapitalScalingBlock capitalScaling={data.capitalScaling} />
        
        {/* Layer 9: Transparency */}
        <TransparencyBlock transparency={data.transparency} />
        
        {/* Advanced (hidden by default) */}
        <AdvancedBlock advanced={data.advanced} />
      </div>
    </div>
  );
};

export default BrainOverviewPage;
