using UnityEngine;

namespace HollowHill
{
    /// <summary>Animasi frame sederhana: uap terowongan, lampu rotator mobil polisi, telepon, lampu gantung.</summary>
    [RequireComponent(typeof(SpriteRenderer))]
    public class SpriteFrameAnimator : MonoBehaviour
    {
        public Sprite[] frames;
        public float fps = 8f;
        public bool randomStart = true;
        public bool pingPong;

        SpriteRenderer sr;
        float t;
        int dir = 1, index;

        void Awake() { sr = GetComponent<SpriteRenderer>(); }

        void OnEnable()
        {
            if (frames == null || frames.Length == 0) return;
            index = randomStart ? Random.Range(0, frames.Length) : 0;
            sr.sprite = frames[index];
        }

        void Update()
        {
            if (frames == null || frames.Length < 2 || fps <= 0f) return;
            t += Time.deltaTime;
            float step = 1f / fps;
            while (t >= step)
            {
                t -= step;
                index += dir;
                if (pingPong)
                {
                    if (index >= frames.Length - 1 || index <= 0) { index = Mathf.Clamp(index, 0, frames.Length - 1); dir = -dir; }
                }
                else index %= frames.Length;
                sr.sprite = frames[index];
            }
        }
    }
}
