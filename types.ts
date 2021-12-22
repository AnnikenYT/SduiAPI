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
    dates: Number[];
    id: number;
    day: number;
    subject_id: number | null;
    subject: ISubject | null;
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
    lesson: ILesson;
    constructor(lesson: ILesson) {
        this.lesson = lesson;
    }
    getId(): number {
        return this.lesson.id;
    }
    getName(): string {
        return this.lesson.meta.displayname;
    }
    getShortcut(): string {
        return this.lesson.meta.shortcut;
    }
    getColor(): TColor {
        return this.lesson.meta.color;
    }
    getKind(): TKind {
        return this.lesson.kind;
    }
    getTimespan(): string {
        return `${this.lesson.time_begins_at} - ${this.lesson.time_ends_at}`;
    }
    getTeachers(): string {
        return this.lesson.teachers.map((teacher: ITeacher) => {
            return teacher.name;
        }).join(', ');
    }
    getGrades(): string {
        return this.lesson.grades.map((grade: IGrade) => {
            return grade.name;
        }).join(', ');
    }
    getBookables(): string {
        return this.lesson.bookables.map((bookable: IBookable) => {
            return bookable.name;
        }).join(', ');
    }
    getComment(): string {
        return this.lesson.comment;
    }
    getCourse(): ICourse {
        return this.lesson.course;
    }
    getSubstitutedTargetLessons(): ILesson[] {
        return this.lesson.substituted_target_lessons;
    }
    getSubstitutedPivot(): ISubstitutedPivot[] {
        return this.lesson.substituted_pivot;
    }
    getReferencedPivot(): any[] {
        return this.lesson.referenced_pivot;
    }
    getReferencedTargetLessons(): any[] {
        return this.lesson.referenced_target_lessons;
    }
}

export class Event extends Lesson {
    constructor(lesson: ILesson) {
        super(lesson);
    }
}

export class Cancled extends Lesson {
    constructor(lesson: ILesson) {
        super(lesson);
    }
}

export type TKind = null | 'EVENT' | 'SWAPED' | 'CANCLED' | 'SUBSTITUTION' | "MOVED_TO" | "BOOKABLE_CHANGE";

export type TLesson = Lesson | Event | Cancled;

export interface ILessons {
    [key: string]: ILesson;
}