export interface Fabrica {
    id: number,
    nombre: string,
    dia: number,
    hora: number,
    minutos: number,
    capital: number,
    beneficio: number,
    coste: number,
    activa: boolean,
    sector: string
}

export interface Asignable {
    id: string,
    nombre: string,
    fatiga: number,
    coste_h: number,
    skills: number[],
    activo: boolean,
    fatigado: number,
    tiempo_fatigado: number,
    fatiga_de_partida: number,
    tiempo_trabajando: number,
    fatiga_inicial: number
}

export interface Trabajador {
    id: string,
    nombre: string,
    apellidos: string,
    fecha_nacimiento: string,
    trabajos_apto: number,
    fatiga: number,
    coste_h: number,
    preferencias_trabajo: number,
    activo: boolean,
    fatigado: number,
    skills: number[],
    tiempo_fatigado: number,
    fatiga_de_partida: number,
    tiempo_trabajando: number,
    fatiga_inicial: number
}

export interface Maquina {
    id: string,
    nombre: string,
    fatiga: number,
    coste_h: number,
    skills: number[],
    activo: boolean,
    fatigado: number,
    tiempo_fatigado: number,
    fatiga_de_partida: number,
    tiempo_trabajando: number,
    fatiga_inicial: number
}

export interface Tarea {
    id: number,
    nombre: string,
    cantidad: number,
    tiempoBase: number,
    duracion: number,
    tiempoActual: number,
    isWorking: boolean,
    beneficio: number,
    coste: number,
    descripcion: string,
    skills: number[],
    tareaPadre: Tarea | undefined,
    tareasHijas: Tarea[],
    isDragging: boolean,
    skillsMatched: number,
    factorFatiga: number,
    factorDuracion: number

    getAsignable(): Asignable | undefined,
    setAsignable(asignable: Asignable): void,
    removeAsignable(): void
}

export interface Skill {
    id: number,
    nombre: string
}