using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class Gun : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private Transform muzzle;
    [SerializeField] private Animator bodyAnimator;
    [SerializeField] private GameObject muzzleFlash;
    [SerializeField] private LineRenderer tracer;
    [SerializeField] private AudioSource audioSource;
    [SerializeField] private TMP_Text ammoText;

    [Header("Effects")]
    [SerializeField] private GameObject wallImpactPrefab;
    [SerializeField] private GameObject bloodImpactPrefab;
    [SerializeField] private float effectTime = 0.05f;
    [SerializeField] private float tracerSpeed = 150f;
    [SerializeField] private float tracerLength = 1.2f;

    [Header("Sounds")]
    [SerializeField] private AudioClip[] shotSounds;
    [SerializeField] private AudioClip[] tailSounds;
    [SerializeField] private AudioClip emptySound;
    [SerializeField] private AudioClip[] reloadSounds;

    [Header("Stats")]
    [SerializeField] private float damage = 25f;
    [SerializeField] private float range = 14f;
    [SerializeField] private float fireDelay = 0.4f;
    [SerializeField] private float spread = 2f;
    [SerializeField] private float reloadTime = 1.8f;

    [Header("Ammo")]
    [SerializeField] private int magazineSize = 12;
    [SerializeField] private int startingSpareMags = 2;

    [Header("Animation")]
    [SerializeField] private bool hasReloadAnimation = false;

    private int roundsInMag;
    private List<int> spareMags = new List<int>();
    private float nextFireTime;
    private bool reloading;

    void Start()
    {
        Physics2D.queriesStartInColliders = false;
        Physics2D.queriesHitTriggers = false;

        roundsInMag = magazineSize;

        for (int i = 0; i < startingSpareMags; i++)
        {
            spareMags.Add(magazineSize);
        }

        if (muzzleFlash != null) { muzzleFlash.SetActive(false); }

        if (tracer != null)
        {
            tracer.positionCount = 2;
            tracer.enabled = false;
        }

        UpdateUI();
    }

    void Update()
    {
        if (reloading) { return; }

        if (Mouse.current.leftButton.wasPressedThisFrame)
        {
            TryShoot();
        }

        if (Keyboard.current.rKey.wasPressedThisFrame)
        {
            StartReload();
        }
    }

    void TryShoot()
    {
        if (Time.time < nextFireTime) { return; }

        if (roundsInMag <= 0)
        {
            Play(emptySound);
            nextFireTime = Time.time + 0.3f;
            return;
        }

        Shoot();
    }

    void Shoot()
    {
        roundsInMag--;
        nextFireTime = Time.time + fireDelay;

        if (bodyAnimator != null) { bodyAnimator.SetTrigger("Shoot"); }
        PlayShot();

        Vector2 direction = Quaternion.Euler(0f, 0f, Random.Range(-spread, spread)) * muzzle.right;
        Vector2 endPoint = (Vector2)muzzle.position + direction * range;

        RaycastHit2D hit = Physics2D.Raycast(muzzle.position, direction, range);

        if (hit.collider != null)
        {
            endPoint = hit.point;

            EnemyHealth enemy = hit.collider.GetComponentInParent<EnemyHealth>();

            if (enemy != null)
            {
                enemy.TakeDamage(damage);
                Spawn(bloodImpactPrefab, hit.point);
            }
            else
            {
                Spawn(wallImpactPrefab, hit.point);
            }
        }

        StartCoroutine(ShowEffects());
        StartCoroutine(FireTracer(muzzle.position, endPoint));
        UpdateUI();
    }

    IEnumerator ShowEffects()
    {
        if (muzzleFlash != null) { muzzleFlash.SetActive(true); }

        yield return new WaitForSeconds(effectTime);

        if (muzzleFlash != null) { muzzleFlash.SetActive(false); }
    }

    IEnumerator FireTracer(Vector2 start, Vector2 end)
    {
        if (tracer == null) { yield break; }

        float distance = Vector2.Distance(start, end);
        Vector2 direction = (end - start).normalized;
        float head = 0f;

        tracer.enabled = true;

        while (head - tracerLength < distance)
        {
            float tail = Mathf.Max(0f, head - tracerLength);
            float frontPoint = Mathf.Min(head, distance);

            tracer.SetPosition(0, start + direction * tail);
            tracer.SetPosition(1, start + direction * frontPoint);

            head += tracerSpeed * Time.deltaTime;
            yield return null;
        }

        tracer.enabled = false;
    }

    void StartReload()
    {
        if (reloading || roundsInMag >= magazineSize) { return; }

        int best = FullestSpareMag();

        if (best < 0)
        {
            Debug.Log("No spare magazines");
            return;
        }

        StartCoroutine(Reload(best));
    }

    IEnumerator Reload(int index)
    {
        reloading = true;
        UpdateUI();

        if (hasReloadAnimation && bodyAnimator != null)
        {
            bodyAnimator.SetTrigger("Reload");
        }

        StartCoroutine(PlayReloadSounds());

        yield return new WaitForSeconds(reloadTime);

        int newRounds = spareMags[index];
        spareMags.RemoveAt(index);

        if (roundsInMag > 0)
        {
            spareMags.Add(roundsInMag);
        }

        roundsInMag = newRounds;
        reloading = false;
        UpdateUI();
    }

    IEnumerator PlayReloadSounds()
    {
        if (audioSource == null || reloadSounds.Length == 0) { yield break; }

        audioSource.pitch = 1f;
        float gap = reloadTime / reloadSounds.Length;

        for (int i = 0; i < reloadSounds.Length; i++)
        {
            Play(reloadSounds[i]);
            yield return new WaitForSeconds(gap);
        }
    }

    int FullestSpareMag()
    {
        int bestIndex = -1;
        int bestRounds = 0;

        for (int i = 0; i < spareMags.Count; i++)
        {
            if (spareMags[i] > bestRounds)
            {
                bestRounds = spareMags[i];
                bestIndex = i;
            }
        }

        return bestIndex;
    }

    public void AddMagazine(int rounds)
    {
        spareMags.Add(rounds);
        UpdateUI();
    }

    void UpdateUI()
    {
        if (ammoText == null) { return; }

        if (reloading)
        {
            ammoText.text = "Reloading";
        }
        else
        {
            ammoText.text = roundsInMag + " / " + spareMags.Count;
        }
    }

    void PlayShot()
    {
        if (audioSource == null) { return; }

        audioSource.pitch = Random.Range(0.95f, 1.05f);

        if (shotSounds.Length > 0)
        {
            audioSource.PlayOneShot(shotSounds[Random.Range(0, shotSounds.Length)]);
        }

        if (tailSounds.Length > 0)
        {
            audioSource.PlayOneShot(tailSounds[Random.Range(0, tailSounds.Length)], 0.7f);
        }
    }

    void Play(AudioClip clip)
    {
        if (audioSource != null && clip != null)
        {
            audioSource.PlayOneShot(clip);
        }
    }

    void Spawn(GameObject prefab, Vector2 point)
    {
        if (prefab != null)
        {
            Instantiate(prefab, point, Quaternion.identity);
        }
    }
}