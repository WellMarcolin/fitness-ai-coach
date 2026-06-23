import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface Props {
  data?: any[]
  loading?: boolean
}

export default function BodyCompositionChart({ data, loading }: Props) {
  if (loading) {
    return <div className="h-64 bg-gray-50 rounded-lg animate-pulse" />
  }

  if (!data || data.length === 0) {
    return (
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center text-gray-400 text-sm">
        Sem dados de composição corporal
      </div>
    )
  }

  const chartData = data.map((d: any) => ({
    date: new Date(d.id).toLocaleDateString('pt-BR'),
    weight: d.weight,
    bodyFat: d.body_fat,
  }))

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis yAxisId="left" tick={{ fontSize: 11 }} label={{ value: 'Peso (kg)', angle: -90, position: 'insideLeft', style: { fontSize: 11 } }} />
          <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} label={{ value: 'BF%', angle: 90, position: 'insideRight', style: { fontSize: 11 } }} />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="weight" stroke="#3b82f6" name="Peso (kg)" dot={false} strokeWidth={2} />
          {chartData[0]?.bodyFat && (
            <Line yAxisId="right" type="monotone" dataKey="bodyFat" stroke="#f59e0b" name="Gordura %" dot={false} strokeWidth={2} />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
