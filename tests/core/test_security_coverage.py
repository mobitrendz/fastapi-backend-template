from app.core import security


def test_render_email_template_coverage():
    context = {"project_name": "Test Project"}
    content = security.render_email_template(
        template_name="test_template.html", context=context
    )
    assert "Test Project" in content
