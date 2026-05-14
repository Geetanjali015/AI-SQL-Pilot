import { useState } from 'react'
import {
  TrendingUp, Database, Lightbulb, AlertTriangle,
  Copy, Check, Code, Clock
} from 'lucide-react'

function ResultsDashboard({ results }) {
  const [activeTab, setActiveTab] = useState('overview')
  const [copiedSQL, setCopiedSQL] = useState(false)

  if (!results) return null

  const {
    mode = 'natural',
    natural_query,
    original_query,
    generated_sql,
    optimized_query,
    is_already_optimized,
    optimizations_applied = [],
    explanation,
    analysis,
    suggested_indexes = [],
    performance = null
  } = results

  // Use optimized_query if available (SQL mode), otherwise use generated_sql (natural mode)
  const final_sql = optimized_query || generated_sql

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedSQL(true)
      setTimeout(() => setCopiedSQL(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: TrendingUp },
    { id: 'queries', label: 'SQL Query', icon: Code },
    { id: 'performance', label: 'Performance', icon: Clock },
  ]

  return (
    <div className="space-y-6">
      {/* Tabs */}
      <div className="card">
        <div className="flex gap-2 overflow-x-auto pb-2">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            )
          })}
        </div>
      </div>

      {/* Tab Content */}
      
      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Natural Query or Original Query */}
          {mode === 'natural' ? (
          <div className="card">
            <h3 className="text-lg font-semibold text-white mb-3">Your Question</h3>
            <p className="text-slate-300 bg-slate-900 rounded-lg p-4 border border-slate-700">
              {natural_query}
            </p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Original Query */}
              <div className="card">
                <h3 className="text-lg font-semibold text-white mb-3">Original Query</h3>
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                  <code className="text-sm text-slate-300 font-mono whitespace-pre-wrap break-words">
                    {original_query}
                  </code>
                </div>
          </div>
              
              {/* Optimization Status */}
              {is_already_optimized ? (
                <div className="card bg-green-500/10 border-green-500/30">
                  <div className="flex items-center gap-3">
                    <div className="bg-green-500/20 p-2 rounded-lg">
                      <Check className="w-5 h-5 text-green-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-green-400">Already Optimized</h3>
                      <p className="text-sm text-slate-300 mt-1">{explanation}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="card bg-primary-500/10 border-primary-500/30">
                  <div className="flex items-center gap-3">
                    <div className="bg-primary-500/20 p-2 rounded-lg">
                      <Lightbulb className="w-5 h-5 text-primary-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-primary-400">Optimizations Applied</h3>
                      {explanation && (
                        <p className="text-sm text-slate-300 mt-1">{explanation}</p>
                      )}
                      {optimizations_applied.length > 0 && (
                        <ul className="mt-2 space-y-1">
                          {optimizations_applied.map((opt, idx) => (
                            <li key={idx} className="text-sm text-slate-300 flex items-start gap-2">
                              <span className="text-primary-400 mt-1">•</span>
                              <span>{opt}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="card">
              <div className="flex items-center gap-3">
                <div className="bg-primary-500/20 p-3 rounded-lg">
                  <Code className="w-6 h-6 text-primary-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Query Complexity</p>
                  <p className="text-xl font-bold text-white capitalize">
                    {analysis?.complexity || 'N/A'}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="bg-yellow-500/20 p-3 rounded-lg">
                  <AlertTriangle className="w-6 h-6 text-yellow-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Issues Found</p>
                  <p className="text-xl font-bold text-white">
                    {analysis?.issues?.length || 0}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="bg-blue-500/20 p-3 rounded-lg">
                  <Database className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-400">Index Suggestions</p>
                  <p className="text-xl font-bold text-white">
                    {suggested_indexes?.length || 0}
                  </p>
                </div>
              </div>
            </div>
            
            {/* Optimizations Applied Count (SQL mode only) */}
            {mode === 'sql' && optimizations_applied.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-3">
                  <div className="bg-purple-500/20 p-3 rounded-lg">
                    <Lightbulb className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-400">Optimizations Applied</p>
                    <p className="text-xl font-bold text-white">
                      {optimizations_applied.length}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Performance Metrics Summary */}
          {performance && (
            <div className="card">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5 text-green-400" />
                Performance Metrics
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                  <p className="text-xs text-slate-400 mb-1">Execution Time</p>
                  <p className="text-2xl font-bold text-white">
                    {performance.execution_time_ms.toFixed(2)} ms
                  </p>
                  {performance.timing_source && (
                    <p className="text-xs text-slate-500 mt-1">
                      {performance.timing_source === 'database' ? 'From database timing' : 'Client-side timing'}
                    </p>
                  )}
                  {performance.db_timing_source && (
                    <p className="text-xs text-slate-500">
                      DB timing source: {performance.db_timing_source === 'explain_analyze' ? 'EXPLAIN ANALYZE' : performance.db_timing_source}
                    </p>
                  )}
                  {performance.total_time_ms !== undefined && performance.total_time_ms !== performance.execution_time_ms && (
                    <p className="text-xs text-slate-500 mt-0.5">
                      Total: {performance.total_time_ms.toFixed(2)}ms
                    </p>
                  )}
                    </div>
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                  <p className="text-xs text-slate-400 mb-1">Memory Used</p>
                  <p className="text-2xl font-bold text-white">
                    {performance.memory_used_mb < 0.01 
                      ? performance.memory_used_mb.toFixed(4) 
                      : performance.memory_used_mb.toFixed(2)} MB
                  </p>
                  {performance.memory_used_mb < 0.01 && (
                    <p className="text-xs text-slate-500 mt-1">
                      ({Math.abs(performance.memory_used_mb * 1024).toFixed(2)} KB)
                    </p>
                  )}
                    </div>
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                  <p className="text-xs text-slate-400 mb-1">CPU Usage</p>
                  <p className="text-2xl font-bold text-white">
                    {performance.cpu_percent.toFixed(2)} %
                  </p>
                </div>
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                  <p className="text-xs text-slate-400 mb-1">Rows Returned</p>
                  <p className="text-2xl font-bold text-white">
                    {performance.row_count.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Queries Tab */}
      {activeTab === 'queries' && (
        <div className="space-y-6">
          {/* Generated/Optimized Query */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                <Code className="w-5 h-5 text-primary-400" />
                {mode === 'sql' ? 'Optimized SQL Query' : 'Generated SQL Query'}
              </h3>
              <button
                onClick={() => copyToClipboard(final_sql)}
                className="btn-secondary flex items-center gap-2 text-sm"
              >
                {copiedSQL ? (
                  <>
                    <Check className="w-4 h-4" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    Copy
                  </>
                )}
              </button>
            </div>
            <pre className="bg-slate-900 rounded-lg p-4 overflow-x-auto border border-slate-700">
              <code className="text-sm text-slate-300 font-mono whitespace-pre-wrap break-words">{final_sql}</code>
            </pre>
            <div className="mt-4 bg-primary-500/10 border border-primary-500/30 rounded-lg p-4">
              <p className="text-sm text-primary-400 font-medium mb-2">ℹ️ About this query</p>
              <p className="text-sm text-slate-300">
                {mode === 'sql' 
                  ? 'This SQL query has been optimized using database context and best practices. It uses the data dictionary to ensure table and column names are correct.'
                  : 'This SQL query has been generated with optimization best practices, including specific column selection, efficient JOINs, and proper filtering. It\'s ready to use in production.'}
              </p>
            </div>
          </div>

          {/* Show Original Query in SQL mode */}
          {mode === 'sql' && original_query && original_query !== final_sql && (
          <div className="card">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <Code className="w-5 h-5 text-slate-400" />
                Original Query (Before Optimization)
              </h3>
              <pre className="bg-slate-900 rounded-lg p-4 overflow-x-auto border border-slate-700">
                <code className="text-sm text-slate-400 font-mono whitespace-pre-wrap break-words">{original_query}</code>
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === 'performance' && (
        <div className="space-y-6">
          {performance ? (
            <>
              {/* Comparison View (SQL Optimization Mode) */}
              {mode === 'sql' && performance.comparison && !is_already_optimized && (
                <div className="card bg-gradient-to-r from-primary-500/10 to-green-500/10 border-primary-500/30">
                  <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                    Performance Comparison: Original vs Optimized
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Original Query Performance */}
                    <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                      <h4 className="text-sm font-semibold text-slate-400 mb-3">Original Query</h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs text-slate-500 mb-1">Execution Time</p>
                          <p className="text-xl font-bold text-slate-300">
                            {performance.comparison.original.execution_time_ms.toFixed(2)} ms
                          </p>
                          {performance.comparison.original.db_execution_time_ms !== undefined && (
                            <p className="text-xs text-slate-500 mt-0.5">
                              DB: {performance.comparison.original.db_execution_time_ms.toFixed(2)}ms
                            </p>
                          )}
                        </div>
                        <div>
                          <p className="text-xs text-slate-500 mb-1">Memory Used</p>
                          <p className="text-xl font-bold text-slate-300">
                            {performance.comparison.original.memory_used_mb < 0.01
                              ? performance.comparison.original.memory_used_mb.toFixed(4)
                              : performance.comparison.original.memory_used_mb.toFixed(2)} MB
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-slate-500 mb-1">CPU Usage</p>
                          <p className="text-xl font-bold text-slate-300">
                            {performance.comparison.original.cpu_percent.toFixed(2)} %
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    {/* Optimized Query Performance */}
                    <div className="bg-green-500/10 rounded-lg p-4 border border-green-500/30">
                      <h4 className="text-sm font-semibold text-green-400 mb-3">Optimized Query</h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs text-slate-500 mb-1">Execution Time</p>
                          <div className="flex items-center gap-2">
                            <p className="text-xl font-bold text-green-400">
                              {performance.execution_time_ms.toFixed(2)} ms
                            </p>
                            {performance.comparison.is_faster && (
                              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                                ↓ {Math.abs(performance.comparison.time_improvement_percent).toFixed(1)}%
                              </span>
                            )}
                          </div>
                          {performance.comparison.is_faster && (
                            <p className="text-xs text-green-400 mt-1">
                              {performance.comparison.time_improvement_ms > 0 ? 'Faster' : 'Slower'} by {Math.abs(performance.comparison.time_improvement_ms).toFixed(2)} ms
                            </p>
                          )}
                          {performance.db_execution_time_ms !== undefined && (
                            <p className="text-xs text-slate-500 mt-0.5">
                              DB: {performance.db_execution_time_ms.toFixed(2)}ms
                            </p>
                          )}
                        </div>
                        <div>
                          <p className="text-xs text-slate-500 mb-1">Memory Used</p>
                          <div className="flex items-center gap-2">
                            <p className="text-xl font-bold text-green-400">
                              {performance.memory_used_mb < 0.01
                                ? performance.memory_used_mb.toFixed(4)
                                : performance.memory_used_mb.toFixed(2)} MB
                            </p>
                            {performance.comparison.uses_less_memory && (
                              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                                ↓ {Math.abs(performance.comparison.memory_improvement_percent).toFixed(1)}%
                              </span>
                            )}
                          </div>
                          {performance.comparison.uses_less_memory && (
                            <p className="text-xs text-green-400 mt-1">
                              Saved {performance.comparison.memory_improvement_mb.toFixed(4)} MB
                            </p>
                          )}
                          {performance.memory_used_mb < 0.01 && (
                            <p className="text-xs text-slate-500 mt-0.5">
                              ({Math.abs(performance.memory_used_mb * 1024).toFixed(2)} KB)
                            </p>
                          )}
                        </div>
                        <div>
                          <p className="text-xs text-slate-500 mb-1">CPU Usage</p>
                          <p className="text-xl font-bold text-green-400">
                            {performance.cpu_percent.toFixed(2)} %
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Improvement Summary */}
                  <div className="mt-4 pt-4 border-t border-slate-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-white">Overall Improvement</p>
                        <p className="text-xs text-slate-400 mt-1">
                          {performance.comparison.is_faster && performance.comparison.uses_less_memory
                            ? 'Query is faster and uses less memory'
                            : performance.comparison.is_faster
                            ? 'Query execution is faster'
                            : performance.comparison.uses_less_memory
                            ? 'Query uses less memory'
                            : 'Performance metrics available'}
                        </p>
                      </div>
                      {(performance.comparison.is_faster || performance.comparison.uses_less_memory) && (
                        <div className="bg-green-500/20 text-green-400 px-4 py-2 rounded-lg border border-green-500/30">
                          <p className="text-sm font-bold">✓ Optimized</p>
              </div>
            )}
          </div>
                  </div>
                </div>
              )}
              
              {/* Performance Metrics Cards */}
              {(mode === 'natural' || is_already_optimized || !performance.comparison) && (
                <div className="card mb-4">
                  <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Clock className="w-5 h-5 text-primary-400" />
                    {mode === 'sql' && is_already_optimized 
                      ? 'Query Performance (Already Optimized)'
                      : mode === 'sql'
                      ? 'Optimized Query Performance'
                      : 'Query Performance'}
                  </h3>
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="bg-green-500/20 p-3 rounded-lg">
                      <Clock className="w-6 h-6 text-green-400" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-slate-400">Execution Time</p>
                      <p className="text-2xl font-bold text-white">
                        {performance.execution_time_ms.toFixed(2)} ms
                      </p>
                      {/* Enhanced timing breakdown */}
                      {(performance.db_execution_time_ms !== undefined || performance.fetch_time_ms !== undefined || performance.conversion_time_ms !== undefined) && (
                        <div className="text-xs text-slate-500 mt-1 space-y-0.5">
                          {performance.db_execution_time_ms !== undefined && (
                            <p>DB: {performance.db_execution_time_ms.toFixed(2)}ms</p>
                          )}
                          {performance.fetch_time_ms !== undefined && (
                            <p>Fetch: {performance.fetch_time_ms.toFixed(2)}ms</p>
                          )}
                          {performance.conversion_time_ms !== undefined && performance.conversion_time_ms > 0 && (
                            <p>Convert: {performance.conversion_time_ms.toFixed(2)}ms</p>
                          )}
                          {performance.network_time_ms !== undefined && performance.network_time_ms > 0 && (
                            <p className="text-slate-400">
                              Network: {performance.network_time_ms.toFixed(2)}ms
                              {performance.network_time_is_heuristic && <span className="text-slate-500 ml-1">(est.)</span>}
                            </p>
                          )}
                        </div>
                      )}
                      {performance.timing_source && (
                        <p className="text-xs text-slate-500 mt-0.5">
                          Source: {performance.timing_source === 'database' ? 'Database' : 'Python'}
                        </p>
                      )}
                      {performance.wall_elapsed_seconds_median !== undefined && (
                        <p className="text-xs text-slate-500 mt-0.5">
                          Wall time: {(performance.wall_elapsed_seconds_median * 1000).toFixed(2)}ms
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="bg-blue-500/20 p-3 rounded-lg">
                      <Database className="w-6 h-6 text-blue-400" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-slate-400">Memory Used</p>
                      <p className="text-2xl font-bold text-white">
                        {performance.memory_used_mb < 0.01 
                          ? performance.memory_used_mb.toFixed(4) 
                          : performance.memory_used_mb.toFixed(2)} MB
                      </p>
                      {performance.memory_used_mb < 0.01 && (
                        <p className="text-xs text-slate-500 mt-1">
                          ({Math.abs(performance.memory_used_mb * 1024).toFixed(2)} KB)
                        </p>
                      )}
                      {performance.memory_calculation_method && (
                        <p className="text-xs text-slate-500 mt-0.5">
                          Method: {performance.memory_calculation_method === 'pympler_full' ? 'Deep size (full)'
                            : performance.memory_calculation_method === 'pympler_sample' ? 'Deep size (sampled)'
                            : performance.memory_calculation_method === 'serialized_sample' ? 'Serialized (sampled)'
                            : performance.memory_calculation_method === 'fallback' ? 'Estimated'
                            : performance.memory_calculation_method}
                        </p>
                      )}
                      {!performance.memory_calculation_method && (
                      <p className="text-xs text-slate-500 mt-0.5">
                        Calculated from result data
                      </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="bg-purple-500/20 p-3 rounded-lg">
                      <TrendingUp className="w-6 h-6 text-purple-400" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-slate-400">CPU Usage</p>
                      <p className="text-2xl font-bold text-white">
                        {performance.cpu_percent?.toFixed(2) || performance.cpu_per_core_percent?.toFixed(2) || '0.00'} %
                      </p>
                      {(performance.cpu_raw_percent !== undefined || performance.cpu_per_core_percent !== undefined) && (
                        <div className="text-xs text-slate-500 mt-1 space-y-0.5">
                          {performance.cpu_per_core_percent !== undefined && (
                            <p>Per-core: {performance.cpu_per_core_percent.toFixed(2)}%</p>
                          )}
                          {performance.cpu_raw_percent !== undefined && performance.cpu_raw_percent > performance.cpu_per_core_percent && (
                            <p>Raw: {performance.cpu_raw_percent.toFixed(2)}%</p>
                          )}
                          {performance.cpu_seconds_used !== undefined && (
                            <p>CPU time: {performance.cpu_seconds_used.toFixed(4)}s</p>
                          )}
                        </div>
                      )}
                      {!performance.cpu_raw_percent && !performance.cpu_per_core_percent && (
                      <p className="text-xs text-slate-500 mt-1">
                        Measured during execution
                      </p>
                      )}
                      {performance.cpu_timing_source && (
                        <p className="text-xs text-slate-500">
                          Source: {performance.cpu_timing_source === 'client_process_psutil' ? 'Client psutil (local process)' : performance.cpu_timing_source}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="bg-yellow-500/20 p-3 rounded-lg">
                      <Database className="w-6 h-6 text-yellow-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-400">Rows Returned</p>
                      <p className="text-2xl font-bold text-white">
                        {performance.row_count.toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Detailed Timing Breakdown */}
              {(performance.fetch_time_ms !== undefined || performance.network_time_ms !== undefined || performance.wall_elapsed_seconds_median !== undefined) && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <Clock className="w-5 h-5 text-blue-400" />
                    Detailed Timing Breakdown
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {performance.db_execution_time_ms !== undefined && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Database Execution</p>
                        <p className="text-lg font-bold text-white">{performance.db_execution_time_ms.toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">
                          {performance.timing_source === 'database' ? 'From database timing' : 'Client-side timing'}
                        </p>
                        {performance.db_timing_source && (
                          <p className="text-xs text-slate-500">
                            Source: {performance.db_timing_source === 'explain_analyze' ? 'EXPLAIN ANALYZE' : performance.db_timing_source}
                          </p>
                        )}
                      </div>
                    )}
                    {performance.fetch_time_ms !== undefined && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Fetch Time</p>
                        <p className="text-lg font-bold text-white">{performance.fetch_time_ms.toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">Time to fetch from database</p>
                      </div>
                    )}
                    {performance.conversion_time_ms !== undefined && performance.conversion_time_ms > 0 && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Conversion Time</p>
                        <p className="text-lg font-bold text-white">{performance.conversion_time_ms.toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">Time to convert results</p>
                      </div>
                    )}
                    {performance.network_time_ms !== undefined && performance.network_time_ms > 0 && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Network Time</p>
                        <p className="text-lg font-bold text-white">{performance.network_time_ms.toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">
                          {performance.network_time_is_heuristic ? 'Estimated' : 'Measured'} transfer time
                        </p>
                      </div>
                    )}
                    {performance.wall_elapsed_seconds_median !== undefined && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Wall Clock Time (Median)</p>
                        <p className="text-lg font-bold text-white">{(performance.wall_elapsed_seconds_median * 1000).toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">Total elapsed time</p>
                      </div>
                    )}
                    {performance.total_time_ms !== undefined && (
                      <div className="bg-slate-900 rounded-lg p-3 border border-slate-700">
                        <p className="text-xs text-slate-400 mb-1">Total Time</p>
                        <p className="text-lg font-bold text-green-400">{performance.total_time_ms.toFixed(2)} ms</p>
                        <p className="text-xs text-slate-500 mt-1">Sum of all operations</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Query Plan */}
              {performance.query_plan && performance.query_plan.length > 0 && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-white mb-4">Query Execution Plan</h3>
                  <div className="bg-slate-900 rounded-lg p-4 border border-slate-700 overflow-x-auto">
                    <pre className="text-sm text-slate-300">
                      {JSON.stringify(performance.query_plan, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Query Results Preview */}
              {performance.data && performance.data.length > 0 && performance.columns && (
            <div className="card">
              <h3 className="text-lg font-semibold text-white mb-4">
                    Query Results ({performance.row_count} rows)
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-slate-700">
                          {performance.columns.map((col, idx) => (
                        <th key={idx} className="text-left py-2 px-3 text-slate-400 font-medium">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                        {performance.data.map((row, idx) => (
                      <tr key={idx} className="border-b border-slate-800 hover:bg-slate-800/50">
                            {performance.columns.map((col, colIdx) => (
                          <td key={colIdx} className="py-2 px-3 text-slate-300">
                                {row[col] !== null && row[col] !== undefined ? String(row[col]) : 'NULL'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                    {(performance.row_count > performance.data.length || performance.data_truncated) && (
                  <div className="text-sm text-slate-400 mt-3 text-center space-y-1">
                        <p>
                        Showing first {performance.data.length} of {performance.row_count} rows
                  </p>
                        {performance.data_truncated && (
                          <p className="text-yellow-400 text-xs">
                            ⚠️ Result set was truncated for display
                          </p>
                        )}
                  </div>
                )}
              </div>
            </div>
          )}
            </>
          ) : (
            <div className="card">
              <div className="text-center py-8">
                <Clock className="w-12 h-12 text-slate-500 mx-auto mb-4" />
                <p className="text-slate-400">Performance metrics not available</p>
                <p className="text-sm text-slate-500 mt-2">
                  The query was not executed or profiling failed
                </p>
              </div>
            </div>
          )}
        </div>
      )}

    </div>
  )
}

export default ResultsDashboard
