using System;
using UnityEngine;

public class BossStats : MonoBehaviour
{
    [Header("Lokasi")]
    public Transform spawnPoint;            // Loc A. Kalau kosong, pakai posisi awal boss
    public float maxDistance = 30f;         // jarak yang dianggap 100% (zona paling jauh)
    public float[] zoneLimits = { 0.33f, 0.66f };

    [Header("Stat dasar")]
    public float baseMaxHealth = 100f;
    public float baseDamage = 10f;

    [Header("Pengali per zona (0 hijau, 1 kuning, 2 merah)")]
    public float[] healthMultiplier = { 1f, 2.5f, 5f };
    public float[] damageMultiplier = { 1f, 1.5f, 2.5f };
    public float[] scaleMultiplier  = { 1f, 1.3f, 1.7f };
    public Color[] zoneColors = { Color.white, new Color(1f, 0.9f, 0.4f), new Color(1f, 0.35f, 0.35f) };

    [Header("Status")]
    [Range(0f, 1f)] public float healthPercent = 1f;
    public float damageTakenMultiplier = 1f;   // diubah controller (mis. saat Recover)
    public float scaleSmooth = 3f;

    public int CurrentZone { get; private set; }
    public float MaxHealth { get; private set; }
    public float Damage { get; private set; }
    public Vector2 SpawnPos { get; private set; }

    public event Action<int> OnZoneChanged;
    public event Action OnDied;

    private Vector3 baseScale;
    private SpriteRenderer[] renderers;
    private bool dead;

    void Awake()
    {
        baseScale = transform.localScale;
        renderers = GetComponentsInChildren<SpriteRenderer>();
        SpawnPos = spawnPoint != null ? (Vector2)spawnPoint.position : (Vector2)transform.position;
        RecalcZone(true);
    }

    void Update()
    {
        if (dead) return;
        RecalcZone(false);

        // ukuran membesar halus sesuai zona
        Vector3 targetScale = baseScale * scaleMultiplier[CurrentZone];
        transform.localScale = Vector3.Lerp(transform.localScale, targetScale, scaleSmooth * Time.deltaTime);
    }

    void RecalcZone(bool force)
    {
        float t = Mathf.Clamp01(Vector2.Distance(transform.position, SpawnPos) / maxDistance);
        int zone = t < zoneLimits[0] ? 0 : (t < zoneLimits[1] ? 1 : 2);

        MaxHealth = baseMaxHealth * healthMultiplier[zone];
        Damage = baseDamage * damageMultiplier[zone];

        if (zone != CurrentZone || force)
        {
            CurrentZone = zone;
            foreach (var r in renderers) r.color = zoneColors[zone];
            OnZoneChanged?.Invoke(zone);
        }
    }

    public void TakeDamage(float amount)
    {
        if (dead) return;
        // persen berkurang = damage / maxHP zona saat ini -> nembak di zona jauh itu boros peluru
        healthPercent -= (amount * damageTakenMultiplier) / MaxHealth;
        if (healthPercent <= 0f)
        {
            healthPercent = 0f;
            dead = true;
            OnDied?.Invoke();
        }
    }
}