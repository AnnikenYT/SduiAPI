export interface ISduiOptions {
    /**
     * The default delta for getLessons
     * @type {number}
     * @default 0
     */
    default_delta?: number;
    /**
     * If the data should be cached or not. Heavily recommended
     * @type {boolean}
     * @default true
     */
    cache_data?: boolean;
    /**
     * If the api url should be different from the default API
     * @type {string}
     * @default "https://api.sdui.app/v1"
     */
    api_url?: string;
    /**
     * Whether to authenticate the user automatically if no token or id is provided. If this is false, and no token or id is provided, you will need to authenticate manually.
     * @type {boolean}
     * @default true
     */
    no_auth?: boolean;
}

export class SduiNotAuthenticatedError extends Error {
    constructor() {
        super("User is not authenticated! Please authenticate with Sdui#authSync() first.");
        this.name = "SduiNotAuthenticatedError";
    }
}

export interface ISduiResponseMeta {
    warnings?: string[];
    errors?: string[];
    success?: string[];
}

export type ISduiStatus = "SUCCESS" | "ERROR" | "WARNING";

export interface ISduiResponse {
    data: ILessons;
    meta: ISduiResponseMeta;
    status: ISduiStatus;
}

export interface IBookable {
    id: number;
    name: string;
    shortcut: string;
}

export interface IGrade {
    id: number;
    name: string;
    shortcut: string;
}

export interface ITeacher {
    id: number;
    name: string;
    shortcut: string;
}

export interface IMeta {
    displayname: string;
    shortcut: string;
    color: TColor;
}

export interface ISubject {
    color?: TColor;
    meta?: IMeta;
    id: number;
    shortcut: string;
    name: string;
}

export type TColor = 'red' | 'green' | 'blue' | 'yellow' | 'orange' | 'purple' | 'pink' | 'brown' | 'grey' | 'black';

export interface ICourse {
    meta: IMeta;
    subject: ISubject;
    id: number;
    name: string | null;
    description: string | null;
    subject_id: number;
}

export interface ISubstitutedPivot {
    id: number;
    lesson_id: number;
    target_id: number;
    lesson_date: string;
}

export interface ILesson {
    bookables: IBookable[];
    grades: IGrade[];
    teachers: ITeacher[];
    dates: number[];
    id: number;
    day: number;
    subject_id?: number;
    subject?: ISubject;
    kind: TKind;
    time_id: number | null;
    comment: string;
    course: ICourse;
    time_begins_at: number;
    time_ends_at: number;
    meta: IMeta;
    substituted_pivot: ISubstitutedPivot[];
    substituted_target_lessons: ILesson[];
    referenced_pivot: any[];
    referenced_target_lessons: any[];
}

export class Lesson {
    public bookables: IBookable[];
    public grades: IGrade[];
    public teachers: ITeacher[];
    public dates: number[];
    public id: number;
    public day: number;
    public subject_id?: number;
    public subject?: ISubject;
    public kind: TKind;
    public time_id: number | null;
    public comment: string;
    public course: ICourse;
    public time_begins_at: number;
    public time_ends_at: number;
    public meta: IMeta;
    public substituted_pivot: ISubstitutedPivot[];
    public substituted_target_lessons: ILesson[];
    public referenced_pivot: any[];
    public referenced_target_lessons: any[];
    constructor(lesson: ILesson) {
        this.bookables = lesson.bookables;
        this.grades = lesson.grades;
        this.teachers = lesson.teachers;
        this.dates = lesson.dates;
        this.id = lesson.id;
        this.day = lesson.day;
        this.subject_id = lesson.subject_id;
        this.subject = lesson.subject;
        this.kind = lesson.kind;
        this.time_id = lesson.time_id;
        this.comment = lesson.comment;
        this.course = lesson.course;
        this.time_begins_at = lesson.time_begins_at;
        this.time_ends_at = lesson.time_ends_at;
        this.meta = lesson.meta;
        this.substituted_pivot = lesson.substituted_pivot;
        this.substituted_target_lessons = lesson.substituted_target_lessons;
        this.referenced_pivot = lesson.referenced_pivot;
        this.referenced_target_lessons = lesson.referenced_target_lessons;
    }
}

export type TKind = null | 'EVENT' | 'SWAPED' | 'CANCLED' | 'SUBSTITUTION' | "MOVED_TO" | "BOOKABLE_CHANGE";


export interface ILessons {
    [key: string]: ILesson;
}

export interface ILead {
	id: number;
	name: string;
	name_alias?: string;
	slink: string;
	state: string;
	uuid: string;
	url?: string;
	street?: string;
	is_beta: boolean;
	is_partner: boolean;
	shortcut: string;
	locale: string;
	environment?: any;
	old_id: number;
	has_sdui: boolean;
	visited_count: number;
	visited_teacher_count: number;
	visited_parent_count: number;
	visited_student_count: number;
	is_locked: number;
	city: string;
	phase: string;
	status: string;
	phase_code: number;
	pipedrive_id: number;
	hubspot_id: string;
}