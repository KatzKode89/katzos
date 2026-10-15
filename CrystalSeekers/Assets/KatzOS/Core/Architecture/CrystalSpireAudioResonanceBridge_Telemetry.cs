using System;
using System.IO;
using UnityEngine;

public partial class CrystalSpireAudioResonanceBridge : MonoBehaviour
{
    [Header("Telemetry Stream")]
    public string telemetryFileName = "primebus_telemetry.json";
    private float pollTimer = 0f;

    void Update()
    {
        pollTimer += Time.deltaTime;
        if (pollTimer >= 2f)
        {
            pollTimer = 0f;
            PollTelemetryStream();
        }
    }

    void PollTelemetryStream()
    {
        string path = Path.Combine(Application.dataPath, "KatzOS/Core/Architecture/" + telemetryFileName);
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            Debug.Log($"[PRIMEBUS TELEMETRY SYNC] Received Packet: {json}");
        }
    }
}
