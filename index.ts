const request = require('request')
const inquirer = require('inquirer')
const fs = require('fs')
var colors = require('colors/safe');

import { Lesson, ILessons, TKind, ILesson, Event, Cancled, TLesson } from "./types"

export function getLessons(TOKEN: string, USER: number, TIMEDELTA: number = 0, CACHE_DATA?: boolean): TLesson[] {
    /**
     * Get all lessons from the API
     * @param TOKEN {string} The API token
     * @param USER {number} The user timetable ID
     * @param TIMEDELTA {number} The time delta in days
     * @param CACHE_DATA {boolean} Whether to cache the data or not
     * @returns {TLesson[]} The lessons
     */
    const API_URL = 'https://api.sdui.app/v1/'
    const TIMETABLE_URL: string = API_URL + 'users/' + USER + '/timetable'

    let l: TLesson[] = []
    // make a request to the API using the token as authentication
    request.get({
        url: TIMETABLE_URL,
        headers: {
            'Authorization': TOKEN
        }
    }, (err: any, res: any, body: any) => {
        if (err) {
            console.log(err)
            return
        }
        var data = JSON.parse(body)
        data = data.data
        const lessons: ILessons = data.lessons
        const lessonsToday: Lesson[] = getLessonsToday(lessons)
        // set l to the lessons today
        l = lessonsToday
    })
    
    function getLessonsToday(lessons: ILessons): TLesson[] {
        const lessonsToday: TLesson[] = []
        // for each lesson in lessons, check if todays utctimetuple is in the lesson's dates
        // get the keys of the lessons object
        const keys = Object.keys(lessons)
        // loop through the keys
        keys.forEach((key: string) => {
            // get the lesson
            let lesson_data = lessons[key]
            // get the utctimetuple of today and convert it to a number
            const utctimetuple = getTimestamp()
            // check if the utctimetuple is in the lesson's dates
            if (lesson_data.dates.includes(utctimetuple)) {
                let lesson = getSpecialLessons(lesson_data)
                // if it is, add the lesson to the lessonsToday array
                lessonsToday.push(lesson)
            }
        })
        return lessonsToday;
    }
    
    function getSpecialLessons(lesson: ILesson): Lesson {
        if (lesson.substituted_target_lessons == []) return new Lesson(lesson)
        for (let sublesson of lesson.substituted_target_lessons) {
            if (sublesson.dates.includes(getTimestamp())) {
                switch (lesson.kind) {
                    case 'EVENT':
                        return new Event(lesson);
                    case "CANCLED":
                        return new Cancled(lesson);
                    default:
                        return new Lesson(lesson);
                }
            }
        }
        return new Lesson(lesson);
    }
    
    
    // Helper Functions
    function getTimestamp(): Number {
        return Date.UTC(new Date().getFullYear(), new Date().getMonth(), new Date().getDate() - 1 + TIMEDELTA, 23) / 1000
    }

    return l
}