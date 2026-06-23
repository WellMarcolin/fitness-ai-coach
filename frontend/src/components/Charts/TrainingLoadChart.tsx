import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface Props {
  data?: any[]
  loading?: boolean
}

export default function TrainingLoadChart({ data, loading }: Props) {
  if (loading) {
    return <div className="h-64 bg-gray-50 rounded-lg animate-pulse" />
  }

  if (!data || data.length === 0) {
    return (
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center text-gray-400 text-sm">
        Sem dados de carga de treino
      </div>
    )
  }

  const chartData = data.map((d: any) => ({
    date: d.start_date_local ? new Date(d.start_date_local).toLocaleDateString('pt-BR') : d.id,
    load: d.icu_training_load || 0,
    ctl: d.icu_ctl,
    atl: d.icu_atl,
    tsb: d.icu_tsb,
  }))

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Legend />
          {chartData[0]?.ctl !== undefined && (
            <>
              <Line type="monotone" dataKey="ctl" stroke="#22c55e" name="CTL" dot={false} strokeWidth={2} />
              <Line type="monotone" dataKey="atl" stroke="#ef4444" name="ATL" dot={false} strokeWidth={2} />
              <Line type="monotone" dataKey="tsb" stroke="#3b82f6" name="TSB" dot={false} strokeWidth={2} strokeDasharray="5 5" />
            </>
          )}
          <Line type="monotone" dataKey="load" stroke="#f59e0b" name="Carga" dot={false} opacity={0.6} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
