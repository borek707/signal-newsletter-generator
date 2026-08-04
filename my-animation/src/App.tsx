import { useEffect, useRef, useState } from "react";

import { PlaybackControls } from "@/components/PlaybackControls";
import { PropertiesPanel, type ControlMeta } from "@/components/PropertiesPanel";
import { ZoomControls } from "@/components/ZoomControls";
import { LottiePlayer, type AnimationSlot } from "@/lib/lottie-player";

const LOTTIE_URL = "/lottie.json";
const CONTROLS_URL = "/controls.json";

function readStartupOptions(search: string): { frame: number | null; paused: boolean } {
  const params = new URLSearchParams(search);
  const rawFrame = params.get("frame");
  const parsed = rawFrame === null ? NaN : Number(rawFrame);
  const frame = Number.isFinite(parsed) ? parsed : null;
  const rawPaused = params.get("paused");
  const paused = rawPaused === null ? frame !== null : rawPaused !== "0";
  return { frame, paused };
}

async function loadControlsMeta(): Promise<Record<string, ControlMeta>> {
  try {
    const res = await fetch(CONTROLS_URL);
    if (!res.ok) return {};
    const data = (await res.json()) as { controls?: ControlMeta[] };
    return Object.fromEntries((data.controls ?? []).map((c) => [c.sid, c]));
  } catch {
    return {};
  }
}

function downloadConfiguredLottie(
  lottieJson: string,
  slots: AnimationSlot[],
  values: Record<string, AnimationSlot["value"]>
) {
  const doc = JSON.parse(lottieJson) as {
    slots?: Record<string, { p?: { k?: unknown; p?: { t?: string } } }>;
  };
  for (const slot of slots) {
    const def = doc.slots?.[slot.id]?.p;
    if (!def) continue;
    const value = values[slot.id] ?? slot.value;
    if (slot.type === "text") {
      if (def.p) def.p.t = value as string;
    } else {
      def.k = value;
    }
  }
  const blob = new Blob([JSON.stringify(doc)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "lottie.json";
  a.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const playerRef = useRef<LottiePlayer | null>(null);
  const lottieJsonRef = useRef<string>("");

  const [playing, setPlaying] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [totalFrames, setTotalFrames] = useState(0);
  const [fps, setFps] = useState(0);
  const [zoom, setZoom] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [slots, setSlots] = useState<AnimationSlot[]>([]);
  const [controlsMeta, setControlsMeta] = useState<Record<string, ControlMeta>>({});

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    let disposed = false;

    (async () => {
      try {
        const res = await fetch(LOTTIE_URL);
        if (!res.ok) throw new Error(`Failed to load ${LOTTIE_URL} (HTTP ${res.status})`);
        const [json, meta] = await Promise.all([res.text(), loadControlsMeta()]);
        if (disposed) return;
        lottieJsonRef.current = json;

        const player = await LottiePlayer.create(canvas, json, {
          onFrame: (frame, total) => {
            setCurrentFrame(frame);
            setTotalFrames(total);
          },
          onPlayStateChange: setPlaying,
          onCameraChange: setZoom,
        });
        if (disposed) {
          player.dispose();
          return;
        }
        playerRef.current = player;
        setTotalFrames(player.getTotalFrames());
        setFps(player.getFps());
        setSlots(player.getSlots());
        setControlsMeta(meta);

        const { frame, paused } = readStartupOptions(window.location.search);
        if (frame !== null) player.seek(frame);
        if (!paused) player.play();
      } catch (e) {
        if (!disposed) setError(e instanceof Error ? e.message : String(e));
      }
    })();

    const observer = new ResizeObserver(() => playerRef.current?.resize());
    observer.observe(canvas);

    return () => {
      disposed = true;
      observer.disconnect();
      playerRef.current?.dispose();
      playerRef.current = null;
    };
  }, []);

  return (
    <div className="dark relative flex h-full w-full items-center justify-center overflow-hidden bg-neutral-950">
      {/* Square 1080x1080 container — canvas + overlay are synced here */}
      <div
        className="relative"
        style={{ width: 1080, height: 1080, maxWidth: "100vmin", maxHeight: "100vmin" }}
      >
        <canvas
          ref={canvasRef}
          data-testid="lottie-canvas"
          className="block h-full w-full"
        />

        {/* Text overlay — positioned in 1080px coordinate space */}
        <div className="pointer-events-none absolute left-0 top-0 z-10 p-[60px]">
          <div
            style={{
              fontFamily: 'ui-sans-serif, system-ui, sans-serif',
              fontSize: 22,
              fontWeight: 600,
              color: 'white',
              letterSpacing: 2,
              opacity: 0,
              animation: 'fadeIn 0.8s ease forwards',
            }}
          >
            SCALAC.AI
          </div>
        </div>

        <div
          className="pointer-events-none absolute left-0 top-0 z-10 flex h-full flex-col justify-center p-[60px]"
          style={{ maxWidth: 560 }}
        >
          <div style={{ fontFamily: 'ui-sans-serif, system-ui, sans-serif', fontWeight: 800, color: 'white', lineHeight: 1.1 }}>
            <div style={{ fontSize: 72, opacity: 0, animation: 'slideUp 0.5s ease 1.2s forwards' }}>Your AI stack</div>
            <div style={{ fontSize: 72, opacity: 0, animation: 'slideUp 0.5s ease 1.5s forwards' }}>grew faster</div>
            <div style={{ fontSize: 72, opacity: 0, animation: 'slideUp 0.5s ease 1.8s forwards' }}>than your</div>
            <div style={{ fontSize: 72, opacity: 0, animation: 'slideUp 0.5s ease 2.1s forwards', display: 'flex', alignItems: 'center', gap: 16 }}>
              architecture
              <span
                style={{
                  display: 'inline-block',
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  background: '#ef4444',
                  opacity: 0,
                  animation: 'bounceIn 0.3s ease 2.6s forwards',
                }}
              />
            </div>
          </div>

          <div
            style={{
              marginTop: 40,
              fontFamily: 'ui-sans-serif, system-ui, sans-serif',
              fontSize: 28,
              color: '#a1a1aa',
              lineHeight: 1.5,
              opacity: 0,
              animation: 'slideUp 0.6s ease 3.0s forwards',
            }}
          >
            We help enterprise teams<br />bring structure to<br />growing AI systems.
          </div>

          <div style={{ marginTop: 48, opacity: 0, animation: 'slideUp 0.6s ease 3.6s forwards' }}>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 12,
                background: '#ef4444',
                color: 'white',
                fontFamily: 'ui-sans-serif, system-ui, sans-serif',
                fontSize: 22,
                fontWeight: 500,
                padding: '16px 32px',
                borderRadius: 8,
                cursor: 'pointer',
              }}
            >
              Book an architecture review →
            </span>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes fadeIn { to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounceIn { 0% { opacity: 0; transform: scale(0); } 60% { opacity: 1; transform: scale(1.3); } 100% { opacity: 1; transform: scale(1); } }
      `}</style>

      {error && (
        <div className="absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="pointer-events-none absolute left-0 top-0 flex justify-end p-4 sm:p-6">
        <ZoomControls
          zoom={zoom}
          onZoomIn={() => playerRef.current?.zoomByCentered(1.2)}
          onZoomOut={() => playerRef.current?.zoomByCentered(1 / 1.2)}
          onReset={() => playerRef.current?.resetCamera()}
        />
      </div>

      <div className="pointer-events-none absolute right-0 top-0 flex max-h-full flex-col p-4 sm:p-6">
        <PropertiesPanel
          slots={slots}
          meta={controlsMeta}
          onScalar={(id, v) => playerRef.current?.setScalarSlot(id, v)}
          onColor={(id, rgba) => playerRef.current?.setColorSlot(id, rgba)}
          onVec2={(id, xy) => playerRef.current?.setVec2Slot(id, xy)}
          onText={(id, v) => playerRef.current?.setTextSlot(id, v)}
          onExport={(values) =>
            downloadConfiguredLottie(lottieJsonRef.current, slots, values)
          }
        />
      </div>

      <div className="pointer-events-none absolute inset-x-0 bottom-0 flex justify-center p-4 sm:p-6">
        <PlaybackControls
          playing={playing}
          currentFrame={currentFrame}
          totalFrames={totalFrames}
          fps={fps}
          onToggle={() => playerRef.current?.toggle()}
          onSeek={(frame) => playerRef.current?.seek(frame)}
        />
      </div>
    </div>
  );
}
