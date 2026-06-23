import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

type DashboardData = {
  current_ctl?: number
  current_atl?: number
  current_tsb?: number
  resting_hr?: number
  hrv?: number
  sleep_avg?: number
  weekly_load?: number
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData>({})
  const [loading, setLoading] = useState(true)

  const { data: activities } = useQuery({
    queryKey: ['activities'],
    queryFn: async () => {
      const res = await axios.get(`${API_URL}/intervals/activities?days=7`)
      return res.data
    },
    refetchInterval: 60000,
  })

  const { data: wellness } = useQuery({
    queryKey: ['wellness'],
    queryFn: async () => {
      const res = await axios.get(`${API_URL}/intervals/wellness?days=7`)
      return res.data
    },
    refetchInterval: 60000,
  })

  useEffect(() => {
    if (activities?.length || wellness?.length) {
      const lastAct = activities?.[activities.length - 1] || {}
      const lastWell = wellness?.[wellness.length - 1] || {}
      setData({
        current_ctl: lastAct.icu_ctl,
        current_atl: lastAct.icu_atl,
        current_tsb: lastAct.icu_tsb,
        resting_hr: lastWell.resting_hr,
        hrv: lastWell.hrv,
        sleep_avg: wellness?.reduce((acc: number, w: any) => acc + (w.sleep_secs || 0), 0) / (wellness?.length || 1) / 3600,
        weekly_load: activities?.reduce((acc: number, a: any) => acc + (a.icu_training_load || 0), 0),
      })
      setLoading(false)
    }
  }, [activities, wellness])

  const metrics = [
    { label: 'CTL (Fitness)', value: data.current_ctl?.toFixed(1), unit: '', color: 'text-green-600', bg: 'bg-green-50' },
    { label: 'ATL (Fadiga)', value: data.current_atl?.toFixed(1), unit: '', color: 'text-red-600', bg: 'bg-red-50' },
    { label: 'TSB (Forma)', value: data.current_tsb?.toFixed(1), unit: '', color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: 'FC Repouso', value: data.resting_hr, unit: 'bpm', color: 'text-purple-600', bg: 'bg-purple-50' },
    { label: 'HRV', value: data.hrv?.toFixed(1), unit: 'ms', color: 'text-indigo-600', bg: 'bg-indigo-50' },
    { label: 'Sono Médio', value: data.sleep_avg?.toFixed(1), unit: 'h', color: 'text-teal-600', bg: 'bg-teal-50' },
    { label: 'Carga Semanal', value: data.weekly_load?.toFixed(0), unit: '', color: 'text-orange-600', bg: 'bg-orange-50' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
        {metrics.map((m) => (
          <div key={m.label} className={`${m.bg} rounded-xl p-4 border border-gray-100`}>
            <p className="text-sm text-gray-500 mb-1">{m.label}</p>
            <p className={`text-2xl font-bold ${m.color}`}>
              {m.value ?? '-'} <span className="text-sm font-normal text-gray-400">{m.unit}</span>
            </p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Últimas Atividades</h2>
          {activities?.length > 0 ? (
            <div className="space-y-3">
              {activities.slice(-5).reverse().map((act: any) => (
                <div key={act.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                  <div>
                    <p className="font-medium text-sm">{act.name || 'Atividade'}</p>
                    <p className="text-xs text-gray-500">
                      {act.type} • {act.distance ? `${(act.distance / 1000).toFixed(1)}km` : ''}
                      {act.moving_time ? ` • ${Math.round(act.moving_time / 60)}min` : ''}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">{act.icu_training_load?.toFixed(0) || '-'}</p>
                    <p className="text-xs text-gray-400">carga</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-sm">Nenhuma atividade encontrada. Conecte o intervals.icu.</p>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Wellness Recente</h2>
          {wellness?.length > 0 ? (
            <div className="space-y-3">
              {wellness.slice(-7).reverse().map((w: any) => (
                <div key={w.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                  <p className="text-sm font-medium">{w.id}</p>
                  <div className="flex gap-4 text-xs text-gray-600">
                    <span>FC: {w.resting_hr || '-'}</span>
                    <span>HRV: {w.hrv || '-'}</span>
                    <span>Sono: {w.sleep_secs ? `${(w.sleep_secs / 3600).toFixed(1)}h` : '-'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-sm">Nenhum dado de wellness encontrado.</p>
          )}
        </div>
      </div>

      <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold mb-2">Próximos Passos</h2>
        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-600">
          <li>Configure suas chaves de API em <strong>Configurações</strong></li>
          <li>Personalize os prompts dos agentes em <strong>Agentes</strong></li>
          <li>Inicie o bot do Telegram e use /insights</li>
          <li>Peça planos de treino, nutricionais e análise metabólica</li>
        </ol>
      </div>
    </div>
  )
}
