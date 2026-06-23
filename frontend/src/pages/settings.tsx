import ApiConfig from '@/components/ApiConfig'

export default function SettingsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Configurações</h1>
      <p className="text-gray-500 mb-6 text-sm">
        Configure as conexões com APIs externas. As credenciais são armazenadas com segurança.
      </p>
      <div className="max-w-2xl">
        <ApiConfig />
      </div>
    </div>
  )
}
