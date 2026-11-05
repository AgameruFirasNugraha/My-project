using UnityEngine;

[RequireComponent(typeof(AudioSource))]
[RequireComponent(typeof(Rigidbody2D))]
public class FootstepSound : MonoBehaviour
{
    [SerializeField] private AudioClip[] clips;
    [SerializeField] private float walkInterval = 0.5f;
    [SerializeField] private float sprintInterval = 0.3f;
    [SerializeField] private float sprintThreshold = 3.5f;

    private AudioSource source;
    private Rigidbody2D rb;
    private float timer;

    void Awake()
    {
        source = GetComponent<AudioSource>();
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        float speed = rb.linearVelocity.magnitude;

        if (speed < 0.1f || clips.Length == 0)
        {
            timer = 0f;
            return;
        }

        float interval = speed > sprintThreshold ? sprintInterval : walkInterval;
        timer = timer + Time.deltaTime;

        if (timer >= interval)
        {
            timer = 0f;
            source.pitch = Random.Range(0.9f, 1.1f);
            source.PlayOneShot(clips[Random.Range(0, clips.Length)]);
        }
    }
}