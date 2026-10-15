using System;
using System.IO;
using UnityEngine;

public class KatzTunezStemController : MonoBehaviour
{
    [Header("KatzTunez Parameters")]
    public float bpm = 135f;
    public string musicalKey = "D Minor";
    public string primeBusHook = "KATZOS_SOVEREIGN_AUDIO_V1.>";

    void Start()
    {
        LoadStemManifest();
    }

    void LoadStemManifest()
    {
        string path = Path.Combine(Application.dataPath, "KatzOS/Audio/katztunez_stems.json");
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            Debug.Log($"[KATZTUNEZ AUDIO] Loaded 135 BPM D Minor pipeline on Bus: {primeBusHook}");
        }
        else
        {
            Debug.LogWarning("[KATZTUNEZ AUDIO] Stem manifest not found in pipeline target.");
        }
    }
}
