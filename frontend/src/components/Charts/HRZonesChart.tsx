import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface Props {
  data?: Record<string, number>
  loading?: boolean
}

const ZONE_COLORS = ['#22c55e', '#84cc16', '#eab308', '#f97316', '#ef4444', '#dc2626']

export default function HRZonesChart({ data, loading }: Props) {
  if (loading) {
    return <div className="h-64 bg-gray-50 rounded-lg animate-pulse" />
  }

  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center text-gray-400 text-sm">
        Sem dados de zonas de FC
      </div>
    )
  }

  const chartData = Object.entries(data).map(([zone, seconds], i) => ({
    zone,
    minutes: Math.round(seconds / 60),
    color: ZONE_COLORS[i % ZONE_COLORS.length],
  }))

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="zone" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} label={{ value: 'minutos', angle: -90, position: 'insideLeft', style: { fontSize: 11 } }} />
          <Tooltip formatter={(value: number) => [`${value} min`, 'Tempo']} />
          <Bar dataKey="minutes" name="Tempo">
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
