const reactComponentUpdateTimeout = 10000
// describe to only test in dev mode

function randomString(strLen) {
  return Math.round(36 ** (strLen + 1) - Math.random() * 36 ** strLen)
    .toString(36)
    .slice(1)
}

function mockAuth() {
  if (Cypress.config('mode') == 'pipeline') {
    cy.intercept('*', req => {
      req.headers.authorization = Cypress.env('TOKEN')
    })
  }
}

describe('Test team CRUD', () => {
  const screenshotFolderName = 'test_team_crud'

  let dummyOrganization,
    dummyValueStream,
    createdTeamId,
    teamName,
    orgName,
    vsName

  beforeEach(mockAuth)

  after(() => {
    cy.apiTearDown(createdTeamId, dummyOrganization, dummyValueStream)
  })

  before(() => {
    teamName = `cypress ${randomString(8)}`
    orgName = `cypress ${randomString(8)}`
    vsName = `cypress ${randomString(8)}`

    cy.apiSetUp(orgName, vsName).then(({ organization, valuestream }) => {
      dummyOrganization = organization
      dummyValueStream = valuestream
    })
  })

  it('can create a team', () => {
    // visit the create team page first
    cy.visitAddTeamPage()
    // fill out the form
    cy.get(`[id="select-an-organization"]`).type(`${orgName}{downarrow}{enter}`)
    cy.get(`[id="select-a-valuestream"]`).type(`${vsName}{downarrow}{enter}`)
    cy.get(`[aria-label="Enter a Team Name"]`).type(teamName)
    cy.get(`[aria-label="Enter the number of members in your team"]`).type('1')
    cy.pickOptionMUIAutocomplete(`[id="select-team-admins"]`)
    cy.pickOptionMUIAutocomplete(`[id="select-feature-boards"]`)

    cy.screenshot(`${screenshotFolderName}/can_create_a_team_pending`)

    // submit, wait for request fo finish and assert that team was created
    cy.intercept('POST', '**/api/v1/teams').as('createTeam')
    cy.get('form').submit()
    cy.wait('@createTeam')
      .then(({ response }) => {
        const { body } = response
        const { id: teamId } = body
        createdTeamId = teamId
      })
      .its('response.statusCode')
      .should('eq', 201)
    // the update and delete button for the team should be visible if the team is created
    cy.get(`[aria-label="update-team-${teamName}"]`, {
      timeout: reactComponentUpdateTimeout,
    }).should('be.visible')
    cy.get(`[aria-label="delete-team-${teamName}"]`, {
      timeout: reactComponentUpdateTimeout,
    }).should('be.visible')

    cy.screenshot(`${screenshotFolderName}/can_create_a_team_done`)
  })

  it('can update a team', () => {
    // visit the admin page
    cy.visitAdminPage()
    // click on update button for the team
    cy.get('[aria-label=Team]').type(teamName)
    cy.get(`[aria-label="update-team-${teamName}"]`).click()
    cy.get(`[aria-label="Enter the number of members in your team"]`).type(
      '{backspace}2',
    )

    cy.screenshot(`${screenshotFolderName}/can_update_a_team_pending`)

    // submit, wait for request to finish and assert the team was updated
    cy.intercept('PUT', `**/api/v1/teams/${createdTeamId}`).as('updateTeam')
    cy.get('form').submit()
    cy.wait('@updateTeam')
      .its('response.statusCode')
      .should('eq', 200)

    cy.waitForAPIDataAfterUserChange()

    cy.get('[aria-label=Team]').type(teamName)
    cy.get(`[aria-label="update-team-${teamName}"]`).click()
    cy.get(`[aria-label="Enter the number of members in your team"]`)
      .should('have.value', '2', { timeout: reactComponentUpdateTimeout })
      .should('be.visible')

    cy.screenshot(`${screenshotFolderName}/can_update_a_team_done`)
  })

  it('can delete a team', () => {
    cy.visitAdminPage()
    cy.get('[aria-label=Team]').type(teamName)
    cy.get(`[aria-label="delete-team-${teamName}"]`).click()
    cy.get(`[aria-labelledby="confirm-dialog"]`).should('exist')
    cy.get(`[aria-label="Enter ${teamName} to Confirm Action"]`).type(
      teamName,
      {
        force: true,
      },
    )

    cy.screenshot(`${screenshotFolderName}/can_delete_a_team_pending`)

    cy.intercept('DELETE', `**/api/v1/teams/${createdTeamId}`).as('deleteTeam')
    cy.get(`[aria-label="Yes Button"]`).click({ force: true })
    cy.wait('@deleteTeam')
      .its('response.statusCode')
      .should('eq', 204)

    cy.get(`[aria-labelledby="confirm-dialog"]`).should('not.exist')
    cy.get(`[aria-label="delete-team-${teamName}"]`).should('not.exist')

    cy.screenshot(`${screenshotFolderName}/can_delete_a_team_done`)
  })
})
