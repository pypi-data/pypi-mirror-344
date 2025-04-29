from vipentium.starter.startz import *
from vipentium.testcases.coreex import *
import datetime
# --------------------------------------------------------------
# Advanced Reporting: JSON and HTML reports
# --------------------------------------------------------------
def generate_json_report(report_file, suite_summary, results):
    # Metadata: capture when the report was generated and some environment details
    metadata = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "framework": "vipentium",
        "framework_version": "1.0.2",  # Update as needed
        "python_version": sys.version.split()[0],
        "os": os.name
    }

    # Calculate statistics from the summary
    total_tests = suite_summary.get("total", 0)
    passed_tests = suite_summary.get("passed", 0)
    failed_tests = suite_summary.get("failed", 0)
    # Calculate average duration per test if total is provided.
    average_duration = suite_summary.get("duration", 0) / total_tests if total_tests > 0 else 0
    # Calculate pass percentage.
    success_rate = f"{(passed_tests / total_tests * 100):.2f}%" if total_tests > 0 else "N/A"

    statistics = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "average_duration": average_duration,
        "success_rate": success_rate
    }

    # Build the advanced report structure
    report = {
        "metadata": metadata,
        "summary": suite_summary,
        "statistics": statistics,
        "results": results
    }

    # Write to file using sort_keys and pretty-print formatting
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, sort_keys=True)

    print(color_text(f"Advanced JSON report generated at {report_file}", MAGENTA))



def generate_html_report(report_file, suite_summary, results):
    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>vipentium Report</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css">
    <style>
      .section {{
        padding: 2rem 1.5rem;
      }}
    </style>
  </head>
  <body>
    <section class="section">
      <div class="container">
        <h1 class="title">Test Summary<br></h1>
        <p class="subtitle">
          Total: {suite_summary['total']}, 
          Passed: {suite_summary['passed']}, 
          Failed: {suite_summary['failed']}, 
          Duration: {suite_summary['duration']:.2f}s
        </p>
        <br>
        <h2 class="title is-4">Test Details</h2>
        <table class="table is-striped is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>Test</th>
              <th>Status</th>
              <th>Duration (s)</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
    """
    for r in results:
        status = "✅ PASS" if r["success"] else "❌ FAIL"
        html += f"""            <tr>
              <td>{r['test']}</td>
              <td>{status}</td>
              <td>{r['duration']:.2f}</td>
              <td>{r['message']}</td>
            </tr>
    """
    html += """          </tbody>
        </table>
      </div>
    </section>
  </body>
</html>
    """
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(color_text(f"HTML report generated at {report_file}", MAGENTA))