from nextpy.psx import component, Link
from nextpy.db import get_session, Job

@component
def JobsHome(props=None):
    props = props or {}
    total_jobs = props.get("total_jobs", 0)
    # Get the featured jobs directly from props instead of useFetch
    featured = props.get("featured_jobs", [])
    
    return (
        <div>
            <section class="px-8 py-16 overflow-hidden text-center text-white shadow-xl rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-700">
                <h1 class="mb-4 text-4xl font-extrabold tracking-tight sm:text-5xl">
                    Find your next <span class="text-yellow-300">dream job</span>
                </h1>
                <p class="max-w-2xl mx-auto mb-8 text-lg text-indigo-100">
                    Browse open positions from top companies. Apply in seconds — no account needed to browse.
                </p>
                <a href="/jobs/browse" class="inline-block px-6 py-3 font-semibold text-gray-900 bg-yellow-400 rounded-lg shadow hover:bg-yellow-300">
                    Browse All Jobs
                </a>
            </section>

            <div class="flex flex-wrap justify-center gap-3 mt-8">
                <a href="/jobs/browse?job_type=full_time" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:border-indigo-500 hover:text-indigo-600">Full-time</a>
                <a href="/jobs/browse?job_type=part_time" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:border-indigo-500 hover:text-indigo-600">Part-time</a>
                <a href="/jobs/browse?job_type=contract" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:border-indigo-500 hover:text-indigo-600">Contract</a>
                <a href="/jobs/browse?experience_level=entry" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:border-indigo-500 hover:text-indigo-600">Entry Level</a>
                <a href="/jobs/browse?experience_level=senior" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:border-indigo-500 hover:text-indigo-600">Senior</a>
            </div>

            <section class="mt-12">
                <h2 class="mb-6 text-2xl font-bold text-gray-900">Featured Jobs</h2>
                {if len(featured) == 0:
                    <p class="text-gray-500">No jobs posted yet. Be the first employer!</p>
                }
                <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {for job in featured:
                        <Link href="/jobs/{job['id']}" class="block p-6 transition bg-white border border-gray-200 shadow-sm group rounded-xl hover:shadow-md hover:border-indigo-300">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="inline-block rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700">
                                    {job.get("job_type", "full_time").replace("_", " ").title()}
                                </span>
                                <span class="inline-block rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
                                    {job.get("experience_level", "mid").title()}
                                </span>
                            </div>
                            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600">{job["title"]}</h3>
                            <p class="mt-1 text-sm text-gray-600">{job["company"]}</p>
                            <div class="flex items-center gap-4 mt-3 text-xs text-gray-500">
                                <span>{job.get("location") or "Remote"}</span>
                            </div>
                        </Link>
                    }
                </div>
            </section>

            <section class="px-8 py-12 mt-16 text-center text-white bg-gray-900 rounded-2xl">
                <h2 class="mb-3 text-2xl font-bold">Are you an employer?</h2>
                <p class="mb-6 text-gray-400">Post your first job listing in under a minute. It's free.</p>
                <a href="/jobs/register" class="inline-block px-6 py-3 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700">
                    Post a Job
                </a>
            </section>
        </div>
    )

def getServerSideProps(context):
    db = get_session()
    try:
        # 1. Count active jobs
        total = db.query(Job).filter(Job.is_active == True).count()
        
        # 2. Query active jobs from the database session
        jobs_query = db.query(Job)
        
        # 3. Convert database objects into dictionaries so Nextpy can pass them to props
        featured_jobs = []
        for job in jobs_query:
            featured_jobs.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "job_type": job.job_type,
                "experience_level": job.experience_level,
                "location": job.location
            })
            
        return {
            "props": {
                "total_jobs": total,
                "featured_jobs": featured_jobs
            }
        }
    finally:
        db.close()

default = JobsHome