import axios from "axios";
import inquirer from "inquirer";
import { Lesson, ISduiOptions, ILead, SduiNotAuthenticatedError } from "./types.js";

export class Sdui {
	private token: string;
	user: number;
	private default_delta: number;
	private cache_data: boolean;
	api_url: string;
	private timetable_url: string;

	constructor(token?: string, user?: number, options?: ISduiOptions) {
		this.token = token || "";
        this.user = user || 0;
        const no_auth = options?.no_auth || false;
        if (!this.token || !this.user) {
            if (no_auth) {
                throw new SduiNotAuthenticatedError();
            } else {
                this.authSync();
            }
        }
		this.default_delta = options?.default_delta || 0;
		this.cache_data = options?.cache_data || true;
		this.api_url = options?.api_url || "https://api.sdui.app/v1";
		this.timetable_url = `${this.api_url}/users/${user}/timetable`;
	}
	/**
	 * Get lessons asyncrhonously. Recommended to use this method instead of getLessons()
	 * NOTE: This method will take a while to complete. This is expected, and cannot be changed.
	 * @param timedelta the delta in days. 0 is today, 1 is tomorrow, -1 is yesterday.
	 * @default options.default_delta || 0
	 */
	public async getLessonsAsync(timedelta?: number): Promise<Lesson[]> {
		let lessons: Lesson[] = [];
		await axios
			.get(this.timetable_url, {
				headers: {
					Authorization: `Bearer ${this.token}`,
				},
			})
			.then((result) => {
				const today = this.getTimestamp(timedelta);
				const keys = Object.keys(result.data);
				keys.forEach((key: string) => {
                    const lesson: Lesson = result.data[key];
                    console.debug(lesson.dates);
					lesson.dates.forEach((date: number) => {
						if (date === today) {
							lessons.push(lesson);
						}
					});
				});
			});
		return lessons;
    }
    
    /**
     * @todo NOT IMPLEMENTED YET
     */
    public getLessonsSync(timedelta?: number): Lesson[] {
        let lessons: Lesson[] = [];
        axios
            .get(this.timetable_url, {
                headers: {
                    Authorization: `Bearer ${this.token}`,
                },
            })
            .then((result) => {
                const today = this.getTimestamp(timedelta);
                const keys = Object.keys(result.data);
                keys.forEach((key: string) => {
                    const lesson: Lesson = result.data[key];
                    lesson.dates.forEach((date: number) => {
                        if (date === today) {
                            lessons.push(lesson);
                        }
                    });
                });
            });
        return lessons;
    }

	private getTimestamp(delta?: number): Number {
		const timedelta = delta || this.default_delta;
		return (
			Date.UTC(
				new Date().getFullYear(),
				new Date().getMonth(),
				new Date().getDate() - 1 + timedelta,
				23
			) / 1000
		);
	}

	public authSync() {
		inquirer
			.prompt([
				{
					type: "list",
					name: "Authentication Method",
					message: "Select an authentication method",
					choices: ["Token", "Username and Password"],
				},
			])
			.then((answers: any) => {
				if (answers.AuthenticationMethod === "Token") {
					this.tokenAuth();
				} else {
					inquirer
						.prompt([
							{
								type: "input",
								name: "School",
								message: "Enter your school zipcode or name",
							},
						])
						.then((answers: any) => {
							axios
								.get(
									`${
										this.api_url
									}/leads?search=${encodeURIComponent(
										answers.School
									)}`
								)
								.then((result) => {
									const leads: ILead[] = result.data.data;
									if (leads.length === 0) {
										console.log("No leads found");
										return;
									}
									inquirer
										.prompt([
											{
												type: "list",
												name: "Lead",
												message: "Select a lead",
												choices: leads.map(
													(lead: ILead) => {
														return {
															name: `${lead.name} (${lead.city})`,
															value: lead.slink,
														};
													}
												),
											},
										])
										.then((answers: any) => {
											this.usernamePasswordAuth(
												answers.Lead
											);
										});
								});
						});
				}
			});
	}
	private tokenAuth() {
		inquirer
			.prompt([
				{
					type: "input",
					name: "Token",
					message: "Enter your token",
				},
			])
			.then((answers: any) => {
				this.token = answers.Token;
			});
	}
	private usernamePasswordAuth(school: number) {
		inquirer
			.prompt([
				{
					type: "input",
					name: "Username",
					message: "Enter your username",
				},
				{
					type: "password",
					name: "Password",
					message: "Enter your password",
				},
			])
			.then((answers: any) => {
				axios
					.post(`${this.api_url}/auth/login`, {
						identifier: answers.Username,
						password: answers.Password,
						slink: school,
						showError: true,
						stayLoggedIn: true,
						token: "",
					})
					.then((result) => {
						this.token = result.data.data.access_token;
						console.log(
							"Authentication successful, getting user data..."
						);
						this.getUserSync();
					})
					.catch((error) => {
						console.log("Authentication failed");
					});
			});
	}
	public getUserSync() {
		axios
			.get(`${this.api_url}/users/self`, {
				headers: {
					Authorization: `Bearer ${this.token}`,
				},
			})
			.then((result) => {
				const response = result.data.data;
				this.user = response.id;
				console.log(
					`Logged in as ${response.firstname} ${response.lastname} (${response.email})`
				);
			})
			.catch((error) => {
				console.log(error.response.data);
			});
    }
}

// const sdui = new Sdui();