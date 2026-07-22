<script lang="ts">
	import { onMount } from 'svelte';
	import { SvelteMap } from 'svelte/reactivity';
	import { geoEquirectangular, geoGraticule10, geoPath } from 'd3-geo';
	import { feature } from 'topojson-client';
	import type { FeatureCollection } from 'geojson';
	import type { BufferGeometry, NormalOrGLBufferAttributes, Points, PointsMaterial } from 'three';
	import world from 'world-atlas/countries-110m.json';
	import type { FirmName, OfficeLocation } from '$lib/data/types';

	interface Props {
		locations: OfficeLocation[];
		active?: boolean;
		onInspect?: (location: OfficeLocation) => void;
	}

	interface GlobeController {
		setActive: (active: boolean) => void;
		updateLocations: (locations: OfficeLocation[]) => void;
	}

	let { locations, active = false, onInspect = () => {} }: Props = $props();
	let hostElement: HTMLDivElement;
	let canvasElement: HTMLCanvasElement;
	let available = $state(true);
	let controller = $state<GlobeController | null>(null);

	const countries = feature(
		world as never,
		world.objects.countries as never
	) as unknown as FeatureCollection;
	const graticule = geoGraticule10();

	$effect(() => {
		controller?.updateLocations(locations);
	});

	$effect(() => {
		controller?.setActive(active);
	});

	onMount(() => {
		let disposed = false;
		let dispose = () => {};

		void (async () => {
			try {
				const THREE = await import('three');
				const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');
				if (disposed) return;

				const renderer = new THREE.WebGLRenderer({
					canvas: canvasElement,
					antialias: true,
					alpha: false,
					powerPreference: 'high-performance'
				});
				renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
				renderer.outputColorSpace = THREE.SRGBColorSpace;
				renderer.toneMapping = THREE.ACESFilmicToneMapping;
				renderer.toneMappingExposure = 1.05;

				const scene = new THREE.Scene();
				scene.background = new THREE.Color('#0c151f');
				const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
				camera.position.set(0, 0.04, 3.72);

				const controls = new OrbitControls(camera, canvasElement);
				controls.enableDamping = true;
				controls.dampingFactor = 0.055;
				controls.enablePan = false;
				controls.minDistance = 2.5;
				controls.maxDistance = 4.8;
				controls.autoRotateSpeed = 0.42;

				const globeGroup = new THREE.Group();
				globeGroup.rotation.set(-0.08, -Math.PI / 2.05, 0);
				scene.add(globeGroup);

				const texture = createMapTexture(THREE);
				const globeGeometry = new THREE.SphereGeometry(1, 128, 72);
				const globeMaterial = new THREE.MeshStandardMaterial({
					map: texture,
					roughness: 0.84,
					metalness: 0.06
				});
				const globe = new THREE.Mesh(globeGeometry, globeMaterial);
				globeGroup.add(globe);

				const atmosphere = new THREE.Mesh(
					new THREE.SphereGeometry(1.045, 96, 56),
					new THREE.MeshBasicMaterial({
						color: '#78a9d5',
						transparent: true,
						opacity: 0.11,
						side: THREE.BackSide,
						blending: THREE.AdditiveBlending
					})
				);
				globeGroup.add(atmosphere);

				scene.add(new THREE.HemisphereLight('#c9e2f5', '#162635', 1.7));
				const keyLight = new THREE.DirectionalLight('#fff3c4', 2.2);
				keyLight.position.set(-2.4, 2.8, 3.4);
				scene.add(keyLight);
				const rimLight = new THREE.DirectionalLight('#5d9fd9', 1.25);
				rimLight.position.set(3, -1.2, -2.5);
				scene.add(rimLight);

				const markerTexture = createMarkerTexture(THREE);
				const markerMaterial = new THREE.PointsMaterial({
					size: 0.07,
					sizeAttenuation: true,
					map: markerTexture,
					transparent: true,
					opacity: 0.86,
					depthWrite: false,
					vertexColors: true,
					blending: THREE.NormalBlending,
					alphaTest: 0.015
				});
				const haloMaterial = new THREE.PointsMaterial({
					size: 0.118,
					sizeAttenuation: true,
					map: markerTexture,
					transparent: true,
					opacity: 0.12,
					depthWrite: false,
					vertexColors: true,
					blending: THREE.AdditiveBlending,
					alphaTest: 0.01
				});
				let markerPoints: Points<
					BufferGeometry<NormalOrGLBufferAttributes>,
					PointsMaterial
				> | null = null;
				let haloPoints: Points<BufferGeometry<NormalOrGLBufferAttributes>, PointsMaterial> | null =
					null;
				let pointGeometry: InstanceType<typeof THREE.BufferGeometry> | null = null;
				let markerLocations: OfficeLocation[] = [];

				const cssFirmVariables: Record<FirmName, string> = {
					Deloitte: '--firm-deloitte',
					PwC: '--firm-pwc',
					EY: '--firm-ey',
					KPMG: '--firm-kpmg'
				};
				const fallbackFirmColors: Record<FirmName, string> = {
					Deloitte: '#469365',
					PwC: '#d4753d',
					EY: '#e4c62f',
					KPMG: '#3977ca'
				};
				const firmColorCache: Partial<Record<FirmName, InstanceType<typeof THREE.Color>>> = {};

				function resolvedFirmColor(firm: FirmName) {
					const cached = firmColorCache[firm];
					if (cached) return cached;
					const cssColor = getComputedStyle(hostElement)
						.getPropertyValue(cssFirmVariables[firm])
						.trim();
					const color = colorFromCss(THREE, cssColor, fallbackFirmColors[firm]);
					firmColorCache[firm] = color;
					return color;
				}

				function positionFor(location: OfficeLocation, radius: number) {
					const phi = THREE.MathUtils.degToRad(90 - location.latitude);
					const theta = THREE.MathUtils.degToRad(location.longitude + 180);
					return new THREE.Vector3(
						-radius * Math.sin(phi) * Math.cos(theta),
						radius * Math.cos(phi),
						radius * Math.sin(phi) * Math.sin(theta)
					);
				}

				function separatedGlobeMarkers(nextLocations: OfficeLocation[]) {
					const coordinateClusters = new SvelteMap<string, OfficeLocation[]>();
					for (const location of nextLocations) {
						const key = `${Math.round(location.latitude * 10)}:${Math.round(location.longitude * 10)}`;
						coordinateClusters.set(key, [...(coordinateClusters.get(key) ?? []), location]);
					}

					const markers: Array<{
						location: OfficeLocation;
						position: InstanceType<typeof THREE.Vector3>;
					}> = [];
					for (const clusterLocations of coordinateClusters.values()) {
						const firmGroups = (['Deloitte', 'PwC', 'EY', 'KPMG'] as FirmName[])
							.map((firm) => ({
								firm,
								locations: clusterLocations.filter((location) => location.firm === firm)
							}))
							.filter((group) => group.locations.length > 0);
						const isSplit = firmGroups.length > 1;
						const centerNormal = positionFor(clusterLocations[0], 1).normalize();
						const referenceAxis =
							Math.abs(centerNormal.y) > 0.9
								? new THREE.Vector3(1, 0, 0)
								: new THREE.Vector3(0, 1, 0);
						const tangentX = new THREE.Vector3()
							.crossVectors(referenceAxis, centerNormal)
							.normalize();
						const tangentY = new THREE.Vector3().crossVectors(centerNormal, tangentX).normalize();
						const spread = firmGroups.length === 2 ? 0.034 : 0.04;

						firmGroups.forEach((group, index) => {
							const position = positionFor(group.locations[0], 1.026);
							if (isSplit) {
								const angle = -Math.PI / 2 + (index * Math.PI * 2) / firmGroups.length;
								position
									.addScaledVector(tangentX, Math.cos(angle) * spread)
									.addScaledVector(tangentY, Math.sin(angle) * spread)
									.normalize()
									.multiplyScalar(1.026);
							}
							markers.push({ location: group.locations[0], position });
						});
					}
					return markers;
				}

				function updateLocations(nextLocations: OfficeLocation[]) {
					if (markerPoints) globeGroup.remove(markerPoints);
					if (haloPoints) globeGroup.remove(haloPoints);
					pointGeometry?.dispose();
					const separatedMarkers = separatedGlobeMarkers(nextLocations);
					markerLocations = separatedMarkers.map((marker) => marker.location);
					const positions: number[] = [];
					const colors: number[] = [];

					for (const { location, position } of separatedMarkers) {
						positions.push(position.x, position.y, position.z);
						const color = resolvedFirmColor(location.firm);
						colors.push(color.r, color.g, color.b);
					}

					pointGeometry = new THREE.BufferGeometry();
					pointGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
					pointGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
					pointGeometry.computeBoundingSphere();
					const nextMarkerPoints = new THREE.Points(pointGeometry, markerMaterial);
					const nextHaloPoints = new THREE.Points(pointGeometry, haloMaterial);
					nextMarkerPoints.renderOrder = 3;
					nextHaloPoints.renderOrder = 2;
					markerPoints = nextMarkerPoints;
					haloPoints = nextHaloPoints;
					globeGroup.add(nextHaloPoints, nextMarkerPoints);
					renderFrame();
				}

				const raycaster = new THREE.Raycaster();
				raycaster.params.Points = { threshold: 0.045 };
				const pointer = new THREE.Vector2();
				function inspectPointer(event: PointerEvent) {
					if (!markerPoints) return;
					const bounds = canvasElement.getBoundingClientRect();
					pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
					pointer.y = -((event.clientY - bounds.top) / bounds.height) * 2 + 1;
					raycaster.setFromCamera(pointer, camera);
					const hit = raycaster.intersectObject(markerPoints)[0];
					if (hit?.index != null && markerLocations[hit.index]) {
						canvasElement.style.cursor = 'pointer';
						onInspect(markerLocations[hit.index]);
					} else {
						canvasElement.style.cursor = 'grab';
					}
				}
				canvasElement.addEventListener('pointermove', inspectPointer, { passive: true });
				canvasElement.addEventListener('pointerdown', () => {
					canvasElement.style.cursor = 'grabbing';
				});
				canvasElement.addEventListener('pointerup', () => {
					canvasElement.style.cursor = 'grab';
				});

				let inViewport = false;
				let modeActive = active;
				const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
				function syncMotion() {
					controls.autoRotate = modeActive && inViewport && !reduceMotion.matches;
				}

				function renderFrame() {
					renderer.render(scene, camera);
				}

				const resizeObserver = new ResizeObserver(([entry]) => {
					const { width, height } = entry.contentRect;
					if (!width || !height) return;
					camera.aspect = width / height;
					camera.updateProjectionMatrix();
					renderer.setSize(width, height, false);
					renderFrame();
				});
				resizeObserver.observe(hostElement);

				const intersectionObserver = new IntersectionObserver(([entry]) => {
					inViewport = entry.isIntersecting;
					syncMotion();
					if (inViewport) renderFrame();
				});
				intersectionObserver.observe(hostElement);
				reduceMotion.addEventListener('change', syncMotion);

				renderer.setAnimationLoop(() => {
					if (!modeActive || !inViewport) return;
					controls.update();
					renderFrame();
				});

				controller = {
					setActive(nextActive) {
						modeActive = nextActive;
						syncMotion();
						renderFrame();
					},
					updateLocations
				};
				updateLocations(locations);
				syncMotion();

				dispose = () => {
					controller = null;
					renderer.setAnimationLoop(null);
					resizeObserver.disconnect();
					intersectionObserver.disconnect();
					reduceMotion.removeEventListener('change', syncMotion);
					canvasElement.removeEventListener('pointermove', inspectPointer);
					controls.dispose();
					texture.dispose();
					globeGeometry.dispose();
					globeMaterial.dispose();
					pointGeometry?.dispose();
					markerTexture.dispose();
					markerMaterial.dispose();
					haloMaterial.dispose();
					renderer.dispose();
				};
			} catch {
				available = false;
			}
		})();

		return () => {
			disposed = true;
			dispose();
		};
	});

	function createMarkerTexture(THREE: typeof import('three')) {
		const markerCanvas = document.createElement('canvas');
		markerCanvas.width = 64;
		markerCanvas.height = 64;
		const context = markerCanvas.getContext('2d');
		if (!context) throw new Error('Canvas context unavailable');
		const glow = context.createRadialGradient(32, 32, 2, 32, 32, 30);
		glow.addColorStop(0, 'rgba(255,255,255,1)');
		glow.addColorStop(0.32, 'rgba(255,255,255,0.96)');
		glow.addColorStop(0.58, 'rgba(255,255,255,0.48)');
		glow.addColorStop(1, 'rgba(255,255,255,0)');
		context.fillStyle = glow;
		context.fillRect(0, 0, 64, 64);
		const texture = new THREE.CanvasTexture(markerCanvas);
		texture.colorSpace = THREE.SRGBColorSpace;
		texture.needsUpdate = true;
		return texture;
	}

	function createMapTexture(THREE: typeof import('three')) {
		const mapCanvas = document.createElement('canvas');
		mapCanvas.width = 1536;
		mapCanvas.height = 768;
		const context = mapCanvas.getContext('2d');
		if (!context) throw new Error('Canvas context unavailable');

		const styles = getComputedStyle(hostElement);
		const ocean = styles.getPropertyValue('--map-ocean').trim() || '#111d29';
		const land = styles.getPropertyValue('--map-land').trim() || '#344a5d';
		const border = styles.getPropertyValue('--map-border').trim() || 'rgba(255,255,255,.28)';
		const grid = styles.getPropertyValue('--map-grid').trim() || 'rgba(255,255,255,.08)';

		context.fillStyle = ocean;
		context.fillRect(0, 0, mapCanvas.width, mapCanvas.height);
		const projection = geoEquirectangular()
			.translate([mapCanvas.width / 2, mapCanvas.height / 2])
			.scale(mapCanvas.width / (2 * Math.PI));
		const renderPath = geoPath(projection, context);

		context.beginPath();
		renderPath(graticule);
		context.strokeStyle = grid;
		context.lineWidth = 1;
		context.stroke();

		for (const country of countries.features) {
			context.beginPath();
			renderPath(country);
			context.fillStyle = land;
			context.fill();
			context.strokeStyle = border;
			context.lineWidth = 0.8;
			context.stroke();
		}

		const texture = new THREE.CanvasTexture(mapCanvas);
		texture.colorSpace = THREE.SRGBColorSpace;
		texture.anisotropy = 8;
		texture.needsUpdate = true;
		return texture;
	}

	function colorFromCss(THREE: typeof import('three'), cssColor: string, fallback: string) {
		const sample = document.createElement('canvas');
		sample.width = 1;
		sample.height = 1;
		const context = sample.getContext('2d');
		if (!context) return new THREE.Color(fallback);
		context.clearRect(0, 0, 1, 1);
		context.fillStyle = fallback;
		if (cssColor) context.fillStyle = cssColor;
		context.fillRect(0, 0, 1, 1);
		const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;
		return new THREE.Color().setRGB(red / 255, green / 255, blue / 255, THREE.SRGBColorSpace);
	}
</script>

<div class="globe-host" bind:this={hostElement}>
	<canvas
		bind:this={canvasElement}
		aria-label={`Interactive 3D globe showing ${locations.length.toLocaleString()} mapped Big Four office locations`}
	></canvas>
	{#if !available}
		<div class="globe-fallback">
			<strong>3D rendering is unavailable</strong>
			<span>The 2D atlas contains the same office locations.</span>
		</div>
	{/if}
</div>

<style>
	.globe-host {
		position: absolute;
		inset: 0;
		min-width: 0;
		background: var(--map-ocean, #111d29);
	}

	canvas {
		display: block;
		width: 100%;
		height: 100%;
		cursor: grab;
		touch-action: none;
	}

	canvas:active {
		cursor: grabbing;
	}

	.globe-fallback {
		position: absolute;
		inset: 0;
		display: grid;
		place-content: center;
		gap: 5px;
		background: var(--map-ocean, #111d29);
		color: var(--text-on-sidebar);
		text-align: center;
	}

	.globe-fallback strong {
		font-size: 14px;
	}

	.globe-fallback span {
		color: var(--text-on-dark-muted);
		font-size: 12px;
	}
</style>
