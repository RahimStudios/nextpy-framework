from nextpy.psx import component, register_component, psx

from pages.documentation.components.introduction import Introduction
from pages.documentation.components.installation import Installation
from pages.documentation.components.quickstart import QuickStart
from pages.documentation.components.project_structure import ProjectStructure
from pages.documentation.components.cli import CLICommands
from pages.documentation.components.routing import RoutingGuide
from pages.documentation.components.state import StateAndHooks
from pages.documentation.components.api_deployment import ApiAndDeployment
from pages.documentation.components.reusable_components import ReusableComponents
from pages.documentation.components.ai import AIAssistantGuide
from pages.documentation.components.psx_guide import PSXGuide
from pages.documentation.components.hooks_guide import HooksGuide
from pages.documentation.components.data_fetching import DataFetchingGuide
from pages.documentation.components.authentication import AuthenticationGuide
from pages.documentation.components.database import DatabaseGuide
from pages.documentation.components.styling import StylingGuide
from pages.documentation.components.ssr_ssg import SSRSSGGuide
from pages.documentation.components.error_handling import ErrorHandlingGuide
from pages.documentation.components.table_of_contents import TableOfContents

# Register components
register_component("Installation", Installation)
register_component("QuickStart", QuickStart)
register_component("ProjectStructure", ProjectStructure)
register_component("CLICommands", CLICommands)
register_component("RoutingGuide", RoutingGuide)
register_component("StateAndHooks", StateAndHooks)
register_component("ApiAndDeployment", ApiAndDeployment)
register_component("ReusableComponents", ReusableComponents)
register_component("AIAssistantGuide", AIAssistantGuide)
register_component("PSXGuide", PSXGuide)
register_component("HooksGuide", HooksGuide)
register_component("DataFetchingGuide", DataFetchingGuide)
register_component("AuthenticationGuide", AuthenticationGuide)
register_component("DatabaseGuide", DatabaseGuide)
register_component("StylingGuide", StylingGuide)
register_component("SSRSSGGuide", SSRSSGGuide)
register_component("ErrorHandlingGuide", ErrorHandlingGuide)
register_component("TableOfContents", TableOfContents)
register_component("Introduction", Introduction)

@component
def DocumentationPage():
    return (
        <>
            <Introduction />
            <Installation />
            <QuickStart />
            <ProjectStructure />
            <CLICommands />
            <PSXGuide />
            <RoutingGuide />
            <StateAndHooks />
            <HooksGuide />
            <DataFetchingGuide />
            <ApiAndDeployment />
            <DatabaseGuide />
            <AuthenticationGuide />
            <StylingGuide />
            <ReusableComponents />
            <SSRSSGGuide />
            <ErrorHandlingGuide />
            <AIAssistantGuide />
        </>
    )


default = DocumentationPage