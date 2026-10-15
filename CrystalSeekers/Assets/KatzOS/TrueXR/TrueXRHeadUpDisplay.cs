using System;
using System.IO;
using UnityEngine;

public class TrueXRHeadUpDisplay : MonoBehaviour
{
    [Header("TrueXR Spatial Configuration")]
    public float targetFramerate = 90f;
    public string activeBus = "KATZOS_SOVEREIGN_AUDIO_V1.>";
    public bool spatialLock = true;

    void Start()
    {
        Application.targetFrameRate = (int)targetFramerate;
        Debug.Log($"[TRUEXR HUD] Initialized 90 FPS Spatial Compositor on Bus: {activeBus} | VRAM Lock: {spatialLock}");
    }
}
